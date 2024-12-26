import base64
from io import BytesIO
from PIL import Image
import numpy as np
import imageio
from copy import deepcopy

import rwmap._frame as frame

Image.MAX_IMAGE_PIXELS = 536870912

def image_width(image_path:str)->int:
    with Image.open(image_path) as img:
        return img.width
    
def image_height(image_path:str)->int:
    with Image.open(image_path) as img:
        return img.height
    
def get_png_text(image:Image.Image)->str:
    byte_arr = BytesIO()
    image.save(byte_arr, format = 'PNG')
    base64_str = base64.b64encode(byte_arr.getvalue()).decode('utf-8')
    return base64_str

def get_image(image_path:str)->Image.Image:
    try:
        image = Image.open(image_path)
    except:
        raise FileNotFoundError(f"Image path {image_path} not found")
    return image

def get_image_from_png_text(png_text:str) -> Image.Image:
    byte_data = base64.b64decode(png_text.encode('utf-8'))
    byte_arr = BytesIO(byte_data)
    image = Image.open(byte_arr)
    return image

def write_file_fromndarray(file_path:str, nparr:np.ndarray) -> None:
    nparr_temp = nparr.astype(np.uint8)
    imageio.imwrite(file_path, nparr_temp)

def image_division(image:Image.Image, division_size:frame.Coordinate) -> tuple[list[np.ndarray], int]:
    width, height = image.size
    div_width, div_height = division_size.output_tuple()

    num_cols = width // div_width
    num_rows = height // div_height

    split_images = []

    for i in range(num_rows):
        for j in range(num_cols):

            left = j * div_width
            right = (j + 1) * div_width

            top = i * div_height
            bottom = (i + 1) * div_height
            
            cell_image = image.crop((left, top, right, bottom))
            cell_image = np.array(cell_image)
            split_images.append(cell_image)

    return split_images, num_cols

def image_division_path(image_path:str, division_size:frame.Coordinate) -> tuple[list[np.ndarray], int]:
    with Image.open(image_path) as image:
        return image_division(image, division_size)

def image_division_coo(image_path:str, division_size:frame.Coordinate, place_grid:frame.Coordinate) -> np.ndarray:
    pixel_ori = place_grid * division_size
    pixel_end = pixel_ori + division_size
    with Image.open(image_path) as image:
        return image.crop((pixel_ori.y(), pixel_ori.x(), pixel_end.y(), pixel_end.x()))
    
def func_fit_compare_ave(np1:np.ndarray, np2:np.ndarray):
    np1_rgb = np.mean(np1, axis = (0, 1))
    np2_rgb = np.mean(np2, axis = (0, 1))
    np_sub = np.abs(np1_rgb[:3] - np2_rgb[:3])
    np_sub_2 = np_sub * np_sub
    np_sum = np.sum(np_sub_2)
    return -np_sum

def add_hsv_gaussian_noise(image:np.ndarray, stddev:list[float], mean:list[float] = [0, 0, 0], randseed:int = -1)->np.ndarray:
    
    import cv2
    if randseed != -1:
        np.random.seed(randseed)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    hsv_channels = cv2.split(hsv_image)

    h, s, v = hsv_channels
    h = h.astype(np.float64)
    s = s.astype(np.float64)
    v = v.astype(np.float64)
    
    noise_h = np.random.normal(mean[0], stddev[0], h.shape).astype(np.float64)
    noise_s = np.random.normal(mean[1], stddev[1], s.shape).astype(np.float64)
    noise_v = np.random.normal(mean[2], stddev[2], v.shape).astype(np.float64)

    if image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        h[alpha_channel > 0] += noise_h[alpha_channel > 0]
        s[alpha_channel > 0] += noise_s[alpha_channel > 0]
        v[alpha_channel > 0] += noise_v[alpha_channel > 0]
    else:

        h += noise_h
        s += noise_s
        v += noise_v

    h = np.clip(h, 0, 179)
    s[s < 0] = 0
    s[s > 255] = 255
    v[v < 0] = 0
    v[v > 255] = 255

    
    hsv_noised = cv2.merge((h, s, v)).astype(np.uint8)

    
    noisy_image_rgb = cv2.cvtColor(hsv_noised, cv2.COLOR_HSV2RGB)
    if image.shape[2] == 4:
        noisy_image_rgba = cv2.merge((noisy_image_rgb, alpha_channel))
        return noisy_image_rgba
    else:
        return noisy_image_rgb
    
def add_hsv_gaussian_noisel(image:np.ndarray, stddev:list[list[float]], stddev_arr:list[np.ndarray], mean:list[float] = [0, 0, 0], randseed:int = -1)->np.ndarray:
    
    import cv2
    
    if randseed != -1:
        np.random.seed(randseed)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    hsv_channels = cv2.split(hsv_image)

    h, s, v = hsv_channels
    h = h.astype(np.float64)
    s = s.astype(np.float64)
    v = v.astype(np.float64)
    noise_h = np.zeros(h.shape, np.float64)
    noise_s = np.zeros(s.shape, np.float64)
    noise_v = np.zeros(v.shape, np.float64)
    for index, stddev_one in enumerate(stddev):
        noise_h = noise_h + np.random.normal(mean[0], stddev_one[0], h.shape).astype(np.float64) * stddev_arr[index]
        noise_s = noise_s + np.random.normal(mean[1], stddev_one[1], s.shape).astype(np.float64) * stddev_arr[index]
        noise_v = noise_v + np.random.normal(mean[2], stddev_one[2], v.shape).astype(np.float64) * stddev_arr[index]

    if image.shape[2] == 4:
        alpha_channel = image[:, :, 3]
        h[alpha_channel > 0] += noise_h[alpha_channel > 0]
        s[alpha_channel > 0] += noise_s[alpha_channel > 0]
        v[alpha_channel > 0] += noise_v[alpha_channel > 0]
    else:

        h += noise_h
        s += noise_s
        v += noise_v

    h = np.clip(h, 0, 179)
    s[s < 0] = 0
    s[s > 255] = 255
    v[v < 0] = 0
    v[v > 255] = 255

    
    hsv_noised = cv2.merge((h, s, v)).astype(np.uint8)

    
    noisy_image_rgb = cv2.cvtColor(hsv_noised, cv2.COLOR_HSV2RGB)
    if image.shape[2] == 4:
        noisy_image_rgba = cv2.merge((noisy_image_rgb, alpha_channel))
        return noisy_image_rgba
    else:
        return noisy_image_rgb