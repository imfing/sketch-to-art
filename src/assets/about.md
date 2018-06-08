**Sketch to Art** helps you create artwork with **cutting-edge AI technology**.

---

<small>
Authors: Shuaibin Zhang, Haoran Su, Tangbo Liu, Xin Fu
</small>

## How It Works

To achieve the goal, there are mainly two steps in the pipeline:

- Reconstruct and generate *real* image from the sketch
- Arbitary style transfer to beautify the result with given result

### Sketch Reconstruction

The principle behind this is called **Conditional Adversarial Networks**, known as [pix2pix](https://phillipi.github.io/pix2pix/), which is able to generate image based on the given image.

![](https://phillipi.github.io/pix2pix/images/teaser_v3.jpg)

![](https://phillipi.github.io/pix2pix/images/edges2cats.jpg)

### Style Transfer

It became known to us with the appearance of [Prisma](https://prisma-ai.com/) app. Typically, we generate an individual model for each pre-defined style. 

Here, we want to go further by using any new picture as the style. So, we adopted the method, [**Universal Style Transfer via Feature Transforms**](https://arxiv.org/abs/1705.08086) proposed in NIPS2017, which enables us to perform arbitary style transfer.

![](https://raw.githubusercontent.com/Yijunmaverick/UniversalStyleTransfer/master/figs/p1.jpg)

## Web App

Hosted on Google Cloud Platform. 
Frontend is built with [Vue.js](https://vuejs.org/). 
Backend server is made with Python.

Entire project is available on [Github](https://github.com/mtobeiyf/sketch-to-art).

## Related Resources

- [pix2pix-tensorflow](https://github.com/affinelayer/pix2pix-tensorflow)

- [Neural-Style-Transfer-Papers](https://github.com/ycjing/Neural-Style-Transfer-Papers)

- [WCT-TF](https://github.com/eridgd/WCT-TF)

![](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://dip.imfing.com)