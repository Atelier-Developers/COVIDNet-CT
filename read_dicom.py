import cv2
import os
import sys
import pydicom
from pydicom import dcmread
import png
import numpy as np
import SimpleITK as sitk


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return 128 + factor * (c - 128)

    return img.point(contrast)


def read_image_any_type(file_path: str, is_temp: bool = True):
    if file_path.split('.')[-1].lower() == 'dcm':
        return read_image_dicom(file_path, is_temp)
    return file_path


def mri_to_png(mri_file, png_file):
    """ Function to convert from a DICOM image to png
        @param mri_file: An opened file like object to read te dicom data
        @param png_file: An opened file like object to write the png data
    """

    # Extracting data from the mri file
    plan = dcmread(mri_file)
    plan.PhotometricInterpretation = 'YBR_FULL'
    shape = plan.pixel_array.shape
    print(f"MRI TO PNG {plan.pixel_array.shape}")

    image_2d = []
    max_val = 0
    for row in plan.pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
            if col > max_val: max_val = col
        image_2d.append(pixels)

    # Rescaling grey scale between 0-255
    image_2d_scaled = []
    for row in image_2d:
        row_scaled = []
        for col in row:
            col_scaled = int((float(col) / float(max_val)) * 255.0)
            row_scaled.append(col_scaled)
        image_2d_scaled.append(row_scaled)

    # Writing the PNG file
    w = png.Writer(shape[1], shape[0], greyscale=True)
    w.write(png_file, image_2d_scaled)


def read_image_dicom(file_path: str, is_temp: bool = True):
    output_filepath = make_new_file_path(file_path, is_temp)
    """ Function to convert an MRI binary file to a
                PNG image file.
                @param mri_file_path: Full path to the mri file
                @param png_file_path: Fill path to the png file
            """
    try:
        # Making sure that the mri file exists
        if not os.path.exists(file_path):
            raise Exception('File "%s" does not exists' % file_path)

        mri_file = open(file_path, 'rb')
        png_file = open(output_filepath, 'wb')

        mri_to_png(mri_file, png_file)

        png_file.close()

        img = cv2.imread(output_filepath)
        img = apply_brightness_contrast(img, 120, 70)
        cv2.imwrite(output_filepath, img)
    except ValueError:
        # ds = dcmread(file_path)
        # ds.PhotometricInterpretation = 'YBR_FULL'
        # img = ds.pixel_array
        # print(f"SECOND: {img.shape}")
        # cv2.imwrite(output_filepath, img)
        img = sitk.ReadImage(file_path, sitk.sitkUInt8)
        # rescale intensity range from [-1000,1000] to [0,255]
        img = sitk.IntensityWindowing(img, -1000, 1000, 0, 255)
        # convert 16-bit pixels to 8-bit
        img = sitk.Cast(img, sitk.sitkUInt8)

        sitk.WriteImage(img, output_filepath)

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
