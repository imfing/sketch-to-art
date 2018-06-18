<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201696-1c1fe926-6cef-11e8-8972-b22e89dba68c.jpg" width="300px" alt="">
</p>

# Sketch to Art

> You could be an artist with AI

[**[Live Demo]**](https://dip.imfing.com)  [**[Report]**](https://github.com/mtobeiyf/sketch-to-art/files/2112403/Artistic_Image_Generation_from_Sketch.pdf) [**[Poster]**](https://github.com/mtobeiyf/sketch-to-art/files/2112417/Poster_Artistic.pdf)

## Introduction

This project can transform your casual sketch to beautiful painting/artwork using modern AI technology.

### Screenshots

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201770-a6b9f35a-6cf0-11e8-8711-916f769c1c9d.jpg" alt="">
</p>

## Framework
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41552981-fbfcfc40-7362-11e8-8deb-fe0d58bc24b2.jpg" width="500px" alt="">
</p>

## Theories

To achieve the goal, there are mainly two steps in the pipeline:

- Reconstruct and generate *real* image from the sketch
- Arbitary style transfer to beautify the result with given result

### Sketch Reconstruction

The principle behind this is called **Conditional Adversarial Networks**, known as [pix2pix](https://phillipi.github.io/pix2pix/), which is able to generate image based on the given image.

![](https://user-images.githubusercontent.com/5097752/41201879-ca11fd6e-6cf2-11e8-91c3-f0cf0f1ac50d.jpg)

**Our Trained Model:**
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41553087-51e71b2c-7363-11e8-95d2-4e11d91658fd.jpg" width="400px" alt="">
</p>


### Style Transfer

It became known to us with the appearance of [Prisma](https://prisma-ai.com/) app. Typically, we generate an individual model for each pre-defined style. Here, we want to go further by using any new picture as the style. So, we adopted the method, [**Universal Style Transfer via Feature Transforms**](https://arxiv.org/abs/1705.08086) proposed in NIPS2017, which enables us to perform arbitary style transfer.
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201821-f40a5cb6-6cf1-11e8-917f-779f4055ffc5.jpg" width="400px" alt="">
</p>

**Our Experiments:**
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41553089-52ad649e-7363-11e8-98a2-9d3cec33f25b.jpg" width="400px" alt="">
</p>

## Combined
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41553091-53a5d2d2-7363-11e8-89ae-6568c864ce27.jpg" width="400px" alt="">
</p>


## Acknowledgments

This is a project of **Digital Image Processing** taught by **Dr. Jia Yan**.

[WCT-TF](https://github.com/eridgd/WCT-TF)

[pix2pix-tensorflow](https://github.com/affinelayer/pix2pix-tensorflow)

[pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

[Neural-Style-Transfer-Papers](https://github.com/ycjing/Neural-Style-Transfer-Papers)

[Vue.js](https://vuejs.org/)

## Authors

Shuaibin Zhang, Haoran Su, Tangbo Liu, Xin Fu

## License
Copyright © 2018, Fing

Released under the [MIT License](https://opensource.org/licenses/MIT).

![](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://dip.imfing.com)
