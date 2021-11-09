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
    cv2.imwrite(make_new_file_path(file_path),img[0])

def make_new_file_path(file_path: str):
    dir = '/'.join(file_path.split('/')[:-1])
    file_name_with_ext = file_path.split('/')[-1]
    file_name = file_name_with_ext.split('.')[0]

    result = f"{dir}/{file_name}.png"
    print(f"res= {result}")
    return result

def test():
    read_image_any_type('F:/pp/kossher/0002.DCM')

if __name__ == '__main__':
    test()
