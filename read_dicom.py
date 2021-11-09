import cv2
import os
import pydicom
import numpy as np

def read_image_any_type(file_path: str):
    if file_path.split('.')[-1].lower() == 'dcm':
        return read_image_dicom(file_path)
    return file_path


def read_image_dicom(file_path: str):
    ds = pydicom.read_file(file_path)
    img = ds.pixel_array
    output_filepath = make_new_file_path(file_path)
    cv2.imwrite(output_filepath,img[0])
    return output_filepath

def make_new_file_path(file_path: str):
    dir = '/'.join(file_path.split('/')[:-1])
    file_name_with_ext = file_path.split('/')[-1]
    file_name = file_name_with_ext.split('.')[0]

    result = f"{dir}/{file_name}.png"
    print(f"res= {result}")
    return result
