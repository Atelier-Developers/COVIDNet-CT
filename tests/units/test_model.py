import unittest
import os
from read_dicom import read_image_any_type
from run_covidnet_ct import COVIDNetCTRunner
import glob


class TestModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestModel, self).__init__(*args, **kwargs)
        self.runner = self.init_model()

    def init_model(self):
        train_kwargs = {}
        model_dir = r"./models/COVID-Net_CT-2_L"
        meta_name = "model.meta"
        ckpt_name = "model"
        meta_file = os.path.join(model_dir, meta_name)
        ckpt = os.path.join(model_dir, ckpt_name)
        input_width = 512
        input_height = 512
        data_dir = "data/COVIDx_CT-2A"

        runner = COVIDNetCTRunner(
            meta_file,
            ckpt=ckpt,
            data_dir=data_dir,
            input_height=input_height,
            input_width=input_width,
            **train_kwargs
        )
        return runner

    def test_inference(self):
        image_files = glob.glob("./assets/*.png",)
        no_crop = True
        heatmap = False
        correct_result = 0
        for image_file in image_files:
            image_class = image_file.split("/")[-1].split("_")[0]
            image_class = 'COVID-19' if image_class == 'c' else 'Normal' if image_class == 'n' else 'Pneumonia'
            result = self.runner.infer(read_image_any_type(image_file, False), not no_crop, heatmap, True)
            if result == image_class:
                correct_result += 1

        print(f"\n\nCorrect Results: {correct_result}, Total: {len(image_files)}, Accuracy: {correct_result / len(image_files)}")

    def test_heatmap_generation(self):
        image_name = "c_covid_case.png"
        image_file = f"./assets/{image_name}"
        no_crop = True
        heatmap = True
        result = self.runner.infer(read_image_any_type(image_file, False), not no_crop, heatmap, True)
        self.assertEqual(result, "COVID-19")
        self.assertTrue(os.path.exists(r"./assets/temp/heatmap.png"))


if __name__ == '__main__':
    unittest.main()
