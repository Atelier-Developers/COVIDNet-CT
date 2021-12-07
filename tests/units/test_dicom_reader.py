import unittest
import os
from read_dicom import read_image_any_type


class TestDicomReader(unittest.TestCase):
    def test_convert_dicom_image(self):
        dicom_path = r"./assets/covid_case1.dcm"
        read_image_any_type(dicom_path, is_temp=False)
        self.assertTrue(os.path.exists(r"./assets/outputs/covid_case1.png"))

    def test_convert_dicom_image_temp(self):
        dicom_path = r"./assets/covid_case2.dcm"
        read_image_any_type(dicom_path)
        self.assertTrue(os.path.exists(r"./assets/temp/covid_case2.png"))


if __name__ == '__main__':
    unittest.main()
