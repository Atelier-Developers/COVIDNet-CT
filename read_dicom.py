import cv2
import os
import sys
import pydicom
import numpy as np


def read_image_any_type(file_path: str, is_temp: bool = True):
    if file_path.split('.')[-1].lower() == 'dcm':
        return read_image_dicom(file_path, is_temp)
    return file_path


def read_image_dicom(file_path: str, is_temp: bool = True):
    ds = pydicom.read_file(file_path)
    img = ds.pixel_array
    output_filepath = make_new_file_path(file_path, is_temp)
    cv2.imwrite(output_filepath, img)
    return output_filepath


def make_new_file_path(file_path: str, is_temp: bool = True):
    dir = '/'.join(file_path.split('/')[:-1])
    file_name_with_ext = file_path.split('/')[-1]
    file_name = file_name_with_ext.split('.')[0]
    target_folder = "temp" if is_temp else "outputs"
    target_dir = f"{dir}/{target_folder}"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    result = f"{target_dir}/{file_name}.png"
    print(f"res= {result}")
    return result


if __name__ == '__main__':
    dcm_image = sys.argv[1]
    is_temp = False
    if len(sys.argv) > 1 and sys.argv[2] == "-temp":
        is_temp = True
    read_image_any_type(dcm_image, is_temp=is_temp)
