# Sketch to Art

> You could be an artist with AI

[**[Live Demo]**](https://dip.imfing.com)

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/41201696-1c1fe926-6cef-11e8-8972-b22e89dba68c.jpg" width="600px" alt="">
</p>

## Introduction

This project can transform your casual sketch to beautiful painting/artwork using modern AI technology.

See the screenshots below:

[TODO]

## Theories

[TODO]

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