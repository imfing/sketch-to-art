import numpy as np
import tensorflow as tf


def upsample_nearest(inputs, scale, data_format='channels_first'):
    shape = tf.shape(inputs)
    if data_format == 'channels_first':
        n, c, h, w = shape[0], shape[1], shape[2], shape[3]
        inputs = tf.transpose(inputs, [0, 2, 3, 1])
        inputs = tf.image.resize_nearest_neighbor(inputs, tf.stack([h*scale, w*scale]))
        return tf.transpose(inputs, [0, 3, 1, 2])
    else:
        n, h, w, c = shape[0], shape[1], shape[2], shape[3]
        return tf.image.resize_nearest_neighbor(inputs, tf.stack([h*scale, w*scale]))


def vgg_preprocess(inputs, data_format='channels_first'):
    """Preprocess image for the VGG network using the convolutional layer

    The layer expects an RGB image with pixel values in [0,1].
    The layer flips the channels (RGB -> BGR), scales the values to [0,255] range,
    and subtracts the VGG mean pixel.
    """
    data_format = 'NCHW' if data_format == 'channels_first' else 'NHWC'
    W = tf.Variable([[[
        [0, 0, 255],
        [0, 255, 0],
        [255, 0, 0]
    ]]], trainable=False, dtype=tf.float32)
    # VGG19 mean pixel value is taken from
    # https://gist.github.com/ksimonyan/211839e770f7b538e2d8#file-readme-md
    b = tf.Variable([-103.939, -116.779, -123.68], trainable=False, dtype=tf.float32)
    conv2d = tf.nn.conv2d(inputs, W, (1,1,1,1), padding='VALID', data_format=data_format)
    return tf.nn.bias_add(conv2d, b, data_format=data_format)
