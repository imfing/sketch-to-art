from __future__ import division, print_function

import os
import argparse
import numpy as np
import tensorflow as tf
import scipy
import time

import sys, os
sys.path.append('./wct/')
from utils import preserve_colors_np
from utils import get_files, get_img, get_img_crop, save_img, resize_to, center_crop
from wct import WCT

checkpoints = ['models/wct/relu5_1', 'models/wct/relu4_1',
               'models/wct/relu3_1', 'models/wct/relu2_1', 'models/wct/relu1_1']
relu_targets = ['relu5_1', 'relu4_1', 'relu3_1', 'relu2_1', 'relu1_1']

# Load the WCT model
wct_model = WCT(checkpoints=checkpoints,
                relu_targets=relu_targets,
                vgg_path='models/wct/vgg_normalised.t7',
                device='/cpu:0',
                ss_patch_size=3,
                ss_stride=1)


def get_stylize_image(content_fullpath, style_fullpath, output_path,
                      content_size=256, style_size=256, alpha=0.6,
                      swap5=False, ss_alpha=0.6, adain=False):
    content_img = get_img(content_fullpath)
    content_img = resize_to(content_img, content_size)

    style_img = get_img(style_fullpath)
    style_img = resize_to(style_img, style_size)

    stylized_rgb = wct_model.predict(
        content_img, style_img, alpha, swap5, ss_alpha, adain)

    save_img(output_path, stylized_rgb)


def main():
    get_stylize_image('./output/pix/_0rf2kww15.png', './styles/2.jpg', 'lala.png')


if __name__ == '__main__':
    main()
