#!/bin/bash

# Download pre-trained models for style transfer
if [ ! -d wct ]; then
    mkdir wct && cd wct
    # Download model for vgg_normalised.t7
    # and relu5_1 relu4_1 relu3_1 relu2_1 relu1_1

    # wget -c -O vgg_normalised.t7 "https://www.dropbox.com/s/kh8izr3fkvhitfn/vgg_normalised.t7?dl=1"
    # wget -c -O models.zip "https://www.dropbox.com/s/ssg39coiih5hjzz/models.zip?dl=1"

    wget "https://github.com/mtobeiyf/sketch-to-art/releases/download/v0.1-models/vgg_normalised.t7"
    wget "https://github.com/mtobeiyf/sketch-to-art/releases/download/v0.1-models/models.zip"
    unzip models.zip
    cd ..
else
    echo "wct directory exists...skip"
fi

# Download trained pix2pix model
if [ ! -e pix2pix.zip ]; then
    wget "https://github.com/mtobeiyf/sketch-to-art/releases/download/v0.1/pix2pix.zip"
    unzip pix2pix.zip
else
    echo "pix2pix model exists...skip"
fi

echo "Finish downloading..."