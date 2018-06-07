from scipy.misc import imread, imresize, imsave
import numpy as np


def load_image(filename, size, crop):
    image = imread(filename, mode='RGB')
    if crop:
        image = central_crop(image)
    if size:
        image = scale_image(image, size)
    return image


def prepare_image(image, normalize=True, data_format='channels_first'):
    if normalize:
        image = image.astype(np.float32)
        image /= 255
    if data_format == 'channels_first':
        image = np.transpose(image, [2, 0, 1]) # HWC --> CHW
    return image


def scale_image(image, size):
    "size specifies the minimum height or width of the output"
    h, w, _ = image.shape
    if h > w:
        image = imresize(image, (h*size//w, size), interp='bilinear')
    else:
        image = imresize(image, (size, w*size//h), interp='bilinear')
    return image


def central_crop(image):
    h, w, _ = image.shape
    minsize = min(h, w)
    h_pad, w_pad = (h - minsize) // 2, (w - minsize) // 2
    image = image[h_pad:h_pad+minsize,w_pad:w_pad+minsize]
    return image


def save_image(filename, image, data_format='channels_first'):
    if data_format == 'channels_first':
        image = np.transpose(image, [1, 2, 0]) # CHW --> HWC
    image *= 255
    image = np.clip(image, 0, 255)
    imsave(filename, image.astype(np.uint8))


def load_mask(filename, h, w):
    mask = imread(filename, mode='L')
    mask = imresize(mask, (h, w), interp='nearest')
    mask = mask.astype(np.uint8)
    mask[mask == 255] = 1
    return mask
