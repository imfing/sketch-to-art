#!/usr/bin/env python
from itertools import product
import argparse
import os

import numpy as np
import tensorflow as tf

from adain.image import load_image, prepare_image, load_mask, save_image
from adain.coral import coral
from adain.nn import build_vgg, build_decoder
from adain.norm import adain
from adain.weights import open_weights
from adain.util import get_filename, get_params, extract_image_names_recursive


def _build_graph(vgg_weights, decoder_weights, alpha, data_format):
    if data_format == 'channels_first':
        image = tf.placeholder(shape=(None, 3, None, None), dtype=tf.float32)
        content = tf.placeholder(shape=(1, 512, None, None), dtype=tf.float32)
        style = tf.placeholder(shape=(1, 512, None, None), dtype=tf.float32)
    else:
        image = tf.placeholder(shape=(None, None, None, 3), dtype=tf.float32)
        content = tf.placeholder(shape=(1, None, None, 512), dtype=tf.float32)
        style = tf.placeholder(shape=(1, None, None, 512), dtype=tf.float32)

    target = adain(content, style, data_format=data_format)
    weighted_target = target * alpha + (1 - alpha) * content

    with open_weights(vgg_weights) as w:
        vgg = build_vgg(image, w, data_format=data_format)
        encoder = vgg['conv4_1']

    if decoder_weights:
        with open_weights(decoder_weights) as w:
            decoder = build_decoder(weighted_target, w, trainable=False,
                                    data_format=data_format)
    else:
        decoder = build_decoder(weighted_target, None, trainable=False,
                                data_format=data_format)

    return image, content, style, target, encoder, decoder

data_format='channels_last'
vgg_weights = 'models/vgg19_weights_normalized.h5',
decoder_weights = 'models/decoder_weights.h5'

image, content, style, target, encoder, decoder = _build_graph(
    vgg_weights='models/vgg19_weights_normalized.h5',
    decoder_weights='models/decoder_weights.h5', 
    alpha=1.0, 
    data_format='channels_last')

def style_transfer(
        content_file=None,
        content_dir=None,
        content_size=512,
        style_file=None,
        style_dir=None,
        style_size=512,
        crop=None,
        preserve_color=None,
        alpha=1.0,
        style_interp_weights=None,
        mask=None,
        output_file=None,
        output_dir='output',
        save_ext='jpg',
        gpu=-1,
        vgg_weights='models/vgg19_weights_normalized.h5',
        decoder_weights='models/decoder_weights.h5'):
    assert bool(content_file) != bool(
        content_dir), 'Either content or content_dir should be given'
    assert bool(style_file) != bool(
        style_dir), 'Either style or style_dir should be given'

    if not os.path.exists(output_dir):
        print('Creating output dir at', output_dir)
        os.mkdir(output_dir)

    # Assume that it is either an h5 file or a name of a TensorFlow checkpoint
    decoder_in_h5 = decoder_weights.endswith('.h5')

    if content_file:
        content_batch = [content_file]
    else:
        assert mask is None, 'For spatial control use the --content option'
        content_batch = extract_image_names_recursive(content_dir)

    if style_file:
        style_batch = [style_file]
    else:
        assert mask is None, 'For spatial control use the --style option'
        style_batch = extract_image_names_recursive(style_dir)

    with tf.Session() as sess:
        if decoder_in_h5:
            sess.run(tf.global_variables_initializer())
        else:
            saver = tf.train.Saver()
            saver.restore(sess, decoder_weights)

        for content_path, style_path in product(content_batch, style_batch):
            content_name = get_filename(content_path)
            content_image = load_image(content_path, content_size, crop)

            if isinstance(style_path, list):  # Style blending/Spatial control
                style_paths = style_path
                style_name = '_'.join(map(get_filename, style_paths))

                # Gather all style images in one numpy array in order to get
                # their activations in one pass
                style_images = None
                for i, style_path in enumerate(style_paths):
                    style_image = load_image(style_path, style_size, crop)
                    if preserve_color:
                        style_image = coral(style_image, content_image)
                    style_image = prepare_image(style_image)
                    if style_images is None:
                        shape = tuple([len(style_paths)]) + style_image.shape
                        style_images = np.empty(shape)
                    assert style_images.shape[1:] == style_image.shape, """Style images must have the same shape"""
                    style_images[i] = style_image
                style_features = sess.run(encoder, feed_dict={
                    image: style_images
                })

                content_image = prepare_image(content_image)
                content_feature = sess.run(encoder, feed_dict={
                    image: content_image[np.newaxis, :]
                })

                # For style blending, get activations for each style then
                # take a weighted sum.
                target_feature = np.zeros(content_feature.shape)
                for style_feature, weight in zip(style_features, style_interp_weights):
                    target_feature += sess.run(target, feed_dict={
                        content: content_feature,
                        style: style_feature[np.newaxis, :]
                    }) * weight
            else:
                style_name = get_filename(style_path)
                style_image = load_image(style_path, style_size, crop)
                if preserve_color:
                    style_image = coral(style_image, content_image)
                # style_image = prepare_image(style_image)
                # content_image = prepare_image(content_image)
                style_image = prepare_image(style_image, True, data_format)
                content_image = prepare_image(content_image, True, data_format)
                style_feature = sess.run(encoder, feed_dict={
                    image: style_image[np.newaxis, :]
                })
                content_feature = sess.run(encoder, feed_dict={
                    image: content_image[np.newaxis, :]
                })
                target_feature = sess.run(target, feed_dict={
                    content: content_feature,
                    style: style_feature
                })

            output = sess.run(decoder, feed_dict={
                content: content_feature,
                target: target_feature
            })

            if not output_file:
                filename = '%s_stylized_%s.%s' % (
                    content_name, style_name, save_ext)
                filename = os.path.join(output_dir, filename)
                save_image(filename, output[0], data_format=data_format)
            else:
                save_image(output_file, output[0], data_format=data_format)
            return True
            # print('Output image saved at', filename)


def get_style_image(content, style, output_file,
                    vgg_weights='models/vgg19_weights_normalized.h5',
                    decoder_weights='models/decoder_weights.h5'):

    output = style_transfer(content_file=content, style_file=style, output_file=output_file,
                            vgg_weights=vgg_weights, decoder_weights=decoder_weights)

    return output


def main():
    print(get_style_image(content='666.jpg',
                          style='styles/sketch.png', output_file='6665.png'))


if __name__ == '__main__':
    main()
