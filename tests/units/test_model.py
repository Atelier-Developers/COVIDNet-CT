import unittest
import os
from read_dicom import read_image_any_type
from run_covidnet_ct import COVIDNetCTRunner


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
        image_file = r"./assets/covid_case.png"
        no_crop = True
        heatmap = False
        heatmap_dir = "covid_case.png"
        result = self.runner.infer(read_image_any_type(image_file, False), not no_crop, heatmap, heatmap_dir, True)
        self.assertEqual(result, "COVID-19")

    def test_heatmap_generation(self):
        image_name = "covid_case.png"
        image_file = f"./assets/{image_name}"
        no_crop = True
        heatmap = True
        result = self.runner.infer(read_image_any_type(image_file, False), not no_crop, heatmap, image_name, True)
        self.assertEqual(result, "COVID-19")
        self.assertTrue(os.path.exists(r"./assets/temp/heatmap.png"))


if __name__ == '__main__':
    unittest.main()
