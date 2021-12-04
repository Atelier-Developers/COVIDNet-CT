import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from data_utils import auto_body_crop, multi_ext_file_iter, IMG_EXTENSIONS
from run_covidnet_ct import create_session, load_graph, load_ckpt

# Tensor names
IMAGE_INPUT_TENSOR = 'Placeholder:0'
TRAINING_PH_TENSOR = 'is_training:0'
FINAL_CONV_TENSOR = 'resnet_model/block_layer4:0'
CLASS_PRED_TENSOR = 'ArgMax:0'
CLASS_PROB_TENSOR = 'softmax_tensor:0'
LOGITS_TENSOR = 'resnet_model/final_dense:0'

# Class names, in order of index
CLASS_NAMES = ('Normal', 'Pneumonia', 'COVID-19')


def load_and_preprocess(image_files, width=512, height=512, autocrop=True):
    """Loads and preprocesses images for inference"""
    images = []
    for image_file in image_files:
        # Load and crop image
        image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        if autocrop:
            image, _ = auto_body_crop(image)
        image = cv2.resize(image, (width, height), cv2.INTER_CUBIC)

        # Convert to float in range [0, 1] and stack to 3-channel
        image = image.astype(np.float32) / 255.0
        image = np.stack((image, image, image), axis=-1)

        # Add to image set
        images.append(image)

    return np.array(images)


def make_gradcam_graph(graph):
    """Adds additional ops to the given graph for Grad-CAM"""
    with graph.as_default():
        # Get required tensors
        final_conv = graph.get_tensor_by_name(FINAL_CONV_TENSOR)
        logits = graph.get_tensor_by_name(LOGITS_TENSOR)
        preds = graph.get_tensor_by_name(CLASS_PRED_TENSOR)

        # Get gradient
        top_class_logits = logits[0, preds[0]]
        grads = tf.gradients(top_class_logits, final_conv)[0]

        # Comute per-channel average gradient
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    return final_conv, pooled_grads


def run_gradcam(graph, final_conv, pooled_grads, sess, image):
    """Creates a Grad-CAM heatmap"""
    with graph.as_default():
        # Run model to compute activations, gradients, predictions, and confidences
        final_conv_out, pooled_grads_out, class_pred, class_prob = sess.run(
            [final_conv, pooled_grads, CLASS_PRED_TENSOR, CLASS_PROB_TENSOR],
            feed_dict={IMAGE_INPUT_TENSOR: image, TRAINING_PH_TENSOR: False})
        final_conv_out = final_conv_out[0]
        class_pred = class_pred[0]
        class_prob = class_prob[0, class_pred]

        # Compute heatmap as gradient-weighted mean of activations
        for i in range(pooled_grads_out.shape[0]):
            final_conv_out[..., i] *= pooled_grads_out[i]
        heatmap = np.mean(final_conv_out, axis=-1)

        # Convert to [0, 1] range
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)

        # Resize to image dimensions
        heatmap = cv2.resize(heatmap, (image.shape[2], image.shape[1]))

    return heatmap, class_pred, class_prob


def run_inference(graph, sess, images, batch_size=1):
    """Runs inference on one or more images"""
    # Create feed dict
    feed_dict = {TRAINING_PH_TENSOR: False}

    # Run inference
    with graph.as_default():
        classes, confidences = [], []
        num_batches = int(np.ceil(images.shape[0] / batch_size))
        for i in range(num_batches):
            # Get batch and add it to the feed dict
            feed_dict[IMAGE_INPUT_TENSOR] = images[i * batch_size:(i + 1) * batch_size, ...]

            # Run images through model
            preds, probs = sess.run([CLASS_PRED_TENSOR, CLASS_PROB_TENSOR], feed_dict=feed_dict)

            # Add results to list
            classes.append(preds)
            confidences.append(probs)

    classes = np.concatenate(classes, axis=0)
    confidences = np.concatenate(confidences, axis=0)

    return classes, confidences


def stacked_bar(ax, probs):
    """Creates a stacked bar graph of slice-wise predictions"""
    x = list(range(probs.shape[0]))
    width = 0.8
    ax.bar(x, probs[:, 0], width, color='g')
    ax.bar(x, probs[:, 1], width, bottom=probs[:, 0], color='r')
    ax.bar(x, probs[:, 2], width, bottom=probs[:, :2].sum(axis=1), color='b')
    ax.set_ylabel('Confidence')
    ax.set_xlabel('Slice Index')
    ax.set_title('Class Confidences by Slice')
    ax.legend(CLASS_NAMES, loc='upper right')
