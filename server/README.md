## Servers

This folder contains separate flask servers:

- `app_pix.py` for pix2pix service
- `app_stylize.py` for style transfer service

Simply run `$ python app_xxx.py` and the corresponding service will listen to the local port. 

## Models

### pix2pix model

`models/pix2pix` should contain pix2pix model exported from the script in [affinelayer/pix2pix-tensorflow](https://github.com/affinelayer/pix2pix-tensorflow). 

Typically there are 5 files: `checkpoint`, `export.data-00000-of-00001`, `export.index`, `export.meta`, `options.json`

### style transfer model

`models/wct` should contain models downloaded by the script `download_models.sh`. There will be 5 directories `relu*_1` and a `vgg_normalised.t7`.