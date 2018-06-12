<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201696-1c1fe926-6cef-11e8-8972-b22e89dba68c.jpg" width="300px" alt="">
</p>

# Sketch to Art

> You could be an artist with AI

[**[Live Demo]**](https://dip.imfing.com)

## Introduction

This project can transform your casual sketch to beautiful painting/artwork using modern AI technology.

### Screenshots

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201770-a6b9f35a-6cf0-11e8-8711-916f769c1c9d.jpg" alt="">
</p>

## Theories

To achieve the goal, there are mainly two steps in the pipeline:

- Reconstruct and generate *real* image from the sketch
- Arbitary style transfer to beautify the result with given result

### Sketch Reconstruction

The principle behind this is called **Conditional Adversarial Networks**, known as [pix2pix](https://phillipi.github.io/pix2pix/), which is able to generate image based on the given image.

![](https://user-images.githubusercontent.com/5097752/41201879-ca11fd6e-6cf2-11e8-91c3-f0cf0f1ac50d.jpg)

### Style Transfer

It became known to us with the appearance of [Prisma](https://prisma-ai.com/) app. Typically, we generate an individual model for each pre-defined style. Here, we want to go further by using any new picture as the style. So, we adopted the method, [**Universal Style Transfer via Feature Transforms**](https://arxiv.org/abs/1705.08086) proposed in NIPS2017, which enables us to perform arbitary style transfer.
<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201821-f40a5cb6-6cf1-11e8-917f-779f4055ffc5.jpg" width="400px" alt="">
</p>

## Installation

### Backend

The server side is powered by Python and Flask. You can see this [simpler example](https://github.com/mtobeiyf/keras-flask-deploy-webapp).
Navigate to the `server` directory and all the files concerning the service and neural networks are there. The two main files:

- `app_pix.py` for pix2pix translation
- `app_stylize.py` for arbitrary style transfer

#### Prerequisites

Make sure you have Python installed. And the following key packages are needed:

```
tensorflow
keras
pillow
flask
gevent
```

#### Run

Simply run with python:

```
$ python app_xxx.py
```

And you could see the output indicating the port it's listening (5001 and 5002). Go to `http://localhost:5001` and you should see the returned information.

### Frontend

You should installed:

- [Node.js](https://nodejs.org)
- [Yarn](https://yarnpkg.com)

```
# Clone the repo
$ git clone git@github.com:mtobeiyf/sketch-to-art.git
$ cd sketch-to-art

# Install dependencies
$ yarn  # or npm install

# Run
$ yarn dev  # or npm run dev
```

Open your favorite browser at `http://localhost:8080`, the site is there.


## Acknowledgments

This is a project of **Digital Image Processing** taught by Dr. Jia Yan.

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