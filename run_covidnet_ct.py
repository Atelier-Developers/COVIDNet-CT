"""
Training/testing/inference script for COVID-Net CT models for COVID-19 detection in CT images.
"""

import os
import sys
import cv2
import json
import shutil
import numpy as np
from math import ceil
import tensorflow as tf
import matplotlib.pyplot as plt
from prometheus_client import CollectorRegistry, multiprocess, start_http_server, push_to_gateway, REGISTRY
from prometheus_client import Histogram, Counter, Summary, Gauge
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import logging
from log_handler import create_logger, merry

logger = create_logger(__name__)
# from main import inference_histogram

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from dataset import COVIDxCTDataset
from data_utils import auto_body_crop
from utils import parse_args
from read_dicom import read_image_any_type

# Dict keys
TRAIN_OP_KEY = 'train_op'
TF_SUMMARY_KEY = 'tf_summaries'
LOSS_KEY = 'loss'

# Tensor names
IMAGE_INPUT_TENSOR = 'Placeholder:0'
LABEL_INPUT_TENSOR = 'Placeholder_1:0'
CLASS_PRED_TENSOR = 'ArgMax:0'
CLASS_PROB_TENSOR = 'softmax_tensor:0'
TRAINING_PH_TENSOR = 'is_training:0'
LOSS_TENSOR = 'add:0'

# Names for train checkpoints
CKPT_NAME = 'model.ckpt'
MODEL_NAME = 'COVID-Net_CT'

# Output directory for storing runs
OUTPUT_DIR = 'output'

# Class names ordered by class index
CLASS_NAMES = ('Normal', 'Pneumonia', 'COVID-19')

inference_histogram = Histogram('inference_latency_seconds', 'Latency of inference', registry=REGISTRY)
inference_pos_covid = Gauge('inference_pos_covid', 'Gauge of positive COVID detections', multiprocess_mode='livesum', registry=REGISTRY)

@merry._try
def dense_grad_filter(gvs):
    """Filter to apply gradient updates to dense layers only"""
    return [(g, v) for g, v in gvs if 'dense' in v.name]

@merry._try
def simple_summary(tag_to_value, tag_prefix=''):
    """Summary object for a dict of python scalars"""
    return tf.Summary(value=[tf.Summary.Value(tag=tag_prefix + tag, simple_value=value)
                             for tag, value in tag_to_value.items() if isinstance(value, (int, float))])

@merry._try
def create_session():
    """Helper function for session creation"""
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    return sess

@merry._try
def load_graph(meta_file):
    """Creates new graph and session"""
    graph = tf.Graph()
    with graph.as_default():
        # Create session and load model
        sess = create_session()

        # Load meta file
        print('Loading meta graph from ' + meta_file)
        saver = tf.train.import_meta_graph(meta_file, clear_devices=True)
    return graph, sess, saver

@merry._try
def load_ckpt(ckpt, sess, saver):
    """Helper for loading weights"""
    # Load weights
    if ckpt is not None:
        print('Loading weights from ' + ckpt)
        saver.restore(sess, ckpt)

@merry._try
def get_lr_scheduler(init_lr, global_step=None, decay_steps=None, schedule_type='cosine'):
    if schedule_type == 'constant':
        return init_lr
    elif schedule_type == 'cosine_decay':
        return tf.train.cosine_decay(init_lr, global_step, decay_steps)
    elif schedule_type == 'exp_decay':
        return tf.train.exponential_decay(init_lr, global_step, decay_steps)


class Metrics:
    """Lightweight class for tracking metrics"""

    def __init__(self):
        num_classes = len(CLASS_NAMES)
        self.labels = list(range(num_classes))
        self.class_names = CLASS_NAMES
        self.confusion_matrix = np.zeros((num_classes, num_classes), dtype=np.uint32)

    @merry._try
    def update(self, y_true, y_pred):
        self.confusion_matrix = self.confusion_matrix + confusion_matrix(y_true, y_pred, labels=self.labels)

    @merry._try
    def reset(self):
        self.confusion_matrix *= 0

    @merry._try
    def values(self):
        conf_matrix = self.confusion_matrix.astype('float')
        metrics = {
            'accuracy': np.diag(conf_matrix).sum() / conf_matrix.sum(),
            'confusion matrix': self.confusion_matrix.copy()
        }
        sensitivity = np.diag(conf_matrix) / np.maximum(conf_matrix.sum(axis=1), 1)
        pos_pred_val = np.diag(conf_matrix) / np.maximum(conf_matrix.sum(axis=0), 1)
        for cls, idx in zip(self.class_names, self.labels):
            metrics['{} {}'.format(cls, 'sensitivity')] = sensitivity[idx]
            metrics['{} {}'.format(cls, 'PPV')] = pos_pred_val[idx]
        return metrics


class COVIDNetCTRunner:
    """Primary training/testing/inference class"""

    def __init__(self, meta_file, ckpt=None, data_dir=None, input_height=512, input_width=512,
                 lr=0.001, momentum=0.9, fc_only=False, max_bbox_jitter=0.025, max_rotation=10,
                 max_shear=0.15, max_pixel_shift=10, max_pixel_scale_change=0.2):
        self.meta_file = meta_file
        self.ckpt = ckpt
        self.input_height = input_height
        self.input_width = input_width
        if data_dir is None:
            self.dataset = None
        else:
            self.dataset = COVIDxCTDataset(
                data_dir,
                image_height=input_height,
                image_width=input_width,
                max_bbox_jitter=max_bbox_jitter,
                max_rotation=max_rotation,
                max_shear=max_shear,
                max_pixel_shift=max_pixel_shift,
                max_pixel_scale_change=max_pixel_scale_change
            )

        # Load graph/checkpoint and add optimizer
        self.graph, self.sess, self.saver = load_graph(self.meta_file)
        with self.graph.as_default():
            self.train_op = self._add_optimizer(lr, momentum, fc_only)
            load_ckpt(self.ckpt, self.sess, self.saver)

    @merry._try
    def trainval(self, epochs, output_dir, batch_size=1, train_split_file='train.txt', val_split_file='val.txt',
                 log_interval=20, val_interval=1000, save_interval=1000):
        """Run training with intermittent validation"""
        ckpt_path = os.path.join(output_dir, CKPT_NAME)
        with self.graph.as_default():
            # Copy original graph without optimizer
            shutil.copy(self.meta_file, output_dir)

            # Create train dataset
            dataset, num_images, batch_size = self.dataset.train_dataset(train_split_file, batch_size)
            data_next = dataset.make_one_shot_iterator().get_next()
            num_iters = ceil(num_images / batch_size) * epochs

            # Create feed and fetch dicts
            feed_dict = {TRAINING_PH_TENSOR: True}
            fetch_dict = {
                TRAIN_OP_KEY: self.train_op,
                LOSS_KEY: LOSS_TENSOR
            }

            # Add summaries
            summary_writer = tf.summary.FileWriter(os.path.join(output_dir, 'events'), self.graph)
            fetch_dict[TF_SUMMARY_KEY] = self._get_train_summary_op()

            # Create validation function
            run_validation = self._get_validation_fn(batch_size, val_split_file)

            # Baseline saving and validation
            print('Saving baseline checkpoint')
            saver = tf.train.Saver()
            saver.save(self.sess, ckpt_path, global_step=0, write_meta_graph=False)
            print('Starting baseline validation')
            metrics = run_validation()
            self._log_and_print_metrics(metrics, 0, summary_writer)

            # Training loop
            print('Training with batch_size {} for {} steps'.format(batch_size, num_iters))
            for i in range(num_iters):
                # Run training step
                data = self.sess.run(data_next)
                feed_dict[IMAGE_INPUT_TENSOR] = data['image']
                feed_dict[LABEL_INPUT_TENSOR] = data['label']
                results = self.sess.run(fetch_dict, feed_dict)

                # Log and save
                step = i + 1
                if step % log_interval == 0:
                    summary_writer.add_summary(results[TF_SUMMARY_KEY], step)
                    print('[step: {}, loss: {}]'.format(step, results[LOSS_KEY]))
                if step % save_interval == 0:
                    print('Saving checkpoint at step {}'.format(step))
                    saver.save(self.sess, ckpt_path, global_step=step, write_meta_graph=False)
                if val_interval > 0 and step % val_interval == 0:
                    print('Starting validation at step {}'.format(step))
                    metrics = run_validation()
                    self._log_and_print_metrics(metrics, step, summary_writer)

            print('Saving checkpoint at last step')
            saver.save(self.sess, ckpt_path, global_step=num_iters, write_meta_graph=False)

    @merry._try
    def test(self, batch_size=1, test_split_file='test.txt', plot_confusion=False):
        """Run test on a checkpoint"""
        with self.graph.as_default():
            # Run test
            print('Starting test')
            metrics = self._get_validation_fn(batch_size, test_split_file)()
            self._log_and_print_metrics(metrics)

            if plot_confusion:
                # Plot confusion matrix
                fig, ax = plt.subplots()
                disp = ConfusionMatrixDisplay(confusion_matrix=metrics['confusion matrix'],
                                              display_labels=CLASS_NAMES)
                disp.plot(include_values=True, cmap='Blues', ax=ax, xticks_rotation='horizontal', values_format='.5g')
                plt.show()

    @inference_histogram.time()
    @merry._try
    def infer(self, image_file, autocrop=True, draw_heatmap=False, retrieve_result=False):
        """Run inference on the given image"""
        # Load and preprocess image
        logger.info("Inferring the provided CT image!")
        from visualization_utils import auto_body_crop, load_and_preprocess, make_gradcam_graph, run_gradcam
        if not draw_heatmap:
            image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
            if autocrop:
                image, _ = auto_body_crop(image)
            image = cv2.resize(image, (self.input_width, self.input_height), cv2.INTER_CUBIC)
            image = image.astype(np.float32) / 255.0
            image = np.expand_dims(np.stack((image, image, image), axis=-1), axis=0)

            # Create feed dict
            feed_dict = {IMAGE_INPUT_TENSOR: image, TRAINING_PH_TENSOR: False}

            # Run inference
            with self.graph.as_default():
                # Add training placeholder if present
                try:
                    self.sess.graph.get_tensor_by_name(TRAINING_PH_TENSOR)
                    feed_dict[TRAINING_PH_TENSOR] = False
                except KeyError:
                    pass

                # Run image through model
                class_, probs = self.sess.run([CLASS_PRED_TENSOR, CLASS_PROB_TENSOR], feed_dict=feed_dict)
                print('\nPredicted Class: ' + CLASS_NAMES[class_[0]])
                print('Confidences: ' + ', '.join(
                    '{}: {}'.format(name, conf) for name, conf in zip(CLASS_NAMES, probs[0])))
                if CLASS_NAMES[class_[0]] == "COVID-19":
                    inference_pos_covid.inc()
                if retrieve_result:
                    return CLASS_NAMES[class_[0]]
        else:

            final_conv, pooled_grads = make_gradcam_graph(self.graph)
            # Prepare image
            image = load_and_preprocess([image_file])

            # Run Grad-CAM
            heatmap, class_pred, class_prob = run_gradcam(
                self.graph, final_conv, pooled_grads, self.sess, image)

            print(CLASS_NAMES[class_pred[0]], end=" ")
            print(' '.join(
                '{:.5f}'.format(conf) for name, conf in zip(CLASS_NAMES, class_prob[0])), end="")

            # Show image
            fig, ax = plt.subplots(1, 1, figsize=(10, 5))
            plt.subplots_adjust(hspace=0.01)
            # ax[0].imshow(image[0])
            plt.suptitle('Predicted Class: {} ({:.3f} confidence)'.format(CLASS_NAMES[class_pred[0]],
                                                                          class_prob[0, class_pred[0]]))
            ax.imshow(image[0])
            ax.imshow(heatmap, cmap='jet', alpha=0.4)
            if not os.path.exists("assets/temp"):
                os.makedirs("assets/temp")
            plt.savefig("assets/temp/heatmap.png", bbox_inches='tight')
            if CLASS_NAMES[class_pred[0]] == "COVID-19":
                inference_pos_covid.inc()
            if retrieve_result:
                return CLASS_NAMES[class_pred[0]]

    @merry._try
    def _add_optimizer(self, learning_rate, momentum, fc_only=False):
        """Adds an optimizer and creates the train op"""
        # Create optimizer
        optimizer = tf.train.MomentumOptimizer(
            learning_rate=learning_rate,
            momentum=momentum
        )

        # Create train op
        global_step = tf.train.get_or_create_global_step()
        loss = self.graph.get_tensor_by_name(LOSS_TENSOR)
        grad_vars = optimizer.compute_gradients(loss)
        if fc_only:
            grad_vars = dense_grad_filter(grad_vars)
        minimize_op = optimizer.apply_gradients(grad_vars, global_step)
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        train_op = tf.group(minimize_op, update_ops)

        # Initialize
        self.sess.run(tf.global_variables_initializer())

        return train_op

    @merry._try
    def _get_validation_fn(self, batch_size=1, val_split_file='val.txt'):
        """Creates validation function to call in self.trainval() or self.test()"""
        # Create val dataset
        dataset, num_images, batch_size = self.dataset.validation_dataset(val_split_file, batch_size)
        dataset = dataset.repeat()  # repeat so there is no need to reconstruct it
        data_next = dataset.make_one_shot_iterator().get_next()
        num_iters = ceil(num_images / batch_size)

        # Create running accuracy metric
        metrics = Metrics()

        # Create feed and fetch dicts
        fetch_dict = {'classes': CLASS_PRED_TENSOR}
        feed_dict = {}

        # Add training placeholder if present
        try:
            self.sess.graph.get_tensor_by_name(TRAINING_PH_TENSOR)
            feed_dict[TRAINING_PH_TENSOR] = False
        except KeyError:
            pass

        def run_validation():
            metrics.reset()
            for i in range(num_iters):
                data = self.sess.run(data_next)
                feed_dict[IMAGE_INPUT_TENSOR] = data['image']
                results = self.sess.run(fetch_dict, feed_dict)
                metrics.update(data['label'], results['classes'])
            return metrics.values()

        return run_validation

    @staticmethod
    def _log_and_print_metrics(metrics, step=None, summary_writer=None, tag_prefix='val/'):
        """Helper for logging and printing"""
        # Pop temporarily and print
        cm = metrics.pop('confusion matrix')
        print('\tconfusion matrix:')
        print('\t' + str(cm).replace('\n', '\n\t'))

        # Print scalar metrics
        for name, val in sorted(metrics.items()):
            print('\t{}: {}'.format(name, val))

        # Log scalar metrics
        if summary_writer is not None:
            summary = simple_summary(metrics, tag_prefix)
            summary_writer.add_summary(summary, step)

        # Restore confusion matrix
        metrics['confusion matrix'] = cm

    @merry._try
    def _get_train_summary_op(self, tag_prefix='train/'):
        loss = self.graph.get_tensor_by_name(LOSS_TENSOR)
        loss_summary = tf.summary.scalar(tag_prefix + 'loss', loss)
        return loss_summary


if __name__ == '__main__':
    logger.info("Bootstrap!")
    # Suppress most TF messages
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    mode, args = parse_args(sys.argv[1:])

    # Create full paths
    meta_file = os.path.join(args.model_dir, args.meta_name)
    ckpt = os.path.join(args.model_dir, args.ckpt_name)

    # Create runner
    if mode == 'train':
        train_kwargs = dict(
            lr=args.learning_rate,
            momentum=args.momentum,
            fc_only=args.fc_only,
            max_bbox_jitter=args.max_bbox_jitter,
            max_rotation=args.max_rotation,
            max_shear=args.max_shear,
            max_pixel_shift=args.max_pixel_shift,
            max_pixel_scale_change=args.max_pixel_scale_change
        )
    else:
        train_kwargs = {}
    runner = COVIDNetCTRunner(
        meta_file,
        ckpt=ckpt,
        data_dir=args.data_dir,
        input_height=args.input_height,
        input_width=args.input_width,
        **train_kwargs
    )

    if mode == 'train':
        # Create output_dir and save run settings
        output_dir = os.path.join(OUTPUT_DIR, MODEL_NAME + args.output_suffix)
        os.makedirs(output_dir, exist_ok=False)
        with open(os.path.join(output_dir, 'run_settings.json'), 'w') as f:
            json.dump(vars(args), f)

        # Run trainval
        runner.trainval(
            args.epochs,
            output_dir,
            batch_size=args.batch_size,
            train_split_file=args.train_split_file,
            val_split_file=args.val_split_file,
            log_interval=args.log_interval,
            val_interval=args.val_interval,
            save_interval=args.save_interval
        )
    elif mode == 'test':
        # Run validation
        split_file = read_image_any_type(args.test_split_file)
        runner.test(
            batch_size=args.batch_size,
            test_split_file=split_file,
            plot_confusion=args.plot_confusion
        )
    elif mode == 'infer':
        # Run inference
        runner.infer(read_image_any_type(args.image_file, False), not args.no_crop, args.heatmap, args.heatmap_dir)
