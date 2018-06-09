from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# coding=utf-8

import stylize

import os
import base64
import json
import re
import time
import glob
import shutil
from io import BytesIO
from PIL import Image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, Response, send_file, make_response
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)


@app.route('/', methods=['GET'])
def index():
    return 'style transfer server running'


@app.route('/getStyleFromId', methods=['GET', 'POST'])
def getStyle():
    if request.method == 'POST':
        sessionId = request.form['id']
        styleId = request.form['style']
        highReality = request.form['highReality']
        highQuality = request.form['highQuality']

        adain = False
        alpha = 0.6
        content_size = 256
        if highReality == 'true':
            adain = True
            alpha = 0.8
        if highQuality == 'true':
            content_size = 512

        pix_out = './output/pix/'+sessionId+'.png'
        style_out = './output/style/'+sessionId+'.png'

        stylize.get_stylize_image(
            pix_out, './styles/'+styleId+'.jpg', style_out,
            content_size=content_size, alpha=alpha, adain=adain)

        with open(os.path.join(os.path.dirname(__file__), style_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return 'invalid request'


@app.route('/getGalleryList', methods=['GET'])
def getGalleryList():
    galleryDir = './gallery'
    files = [os.path.basename(x) for x in sorted(
        glob.glob(os.path.join(galleryDir, '*.png')), reverse=True)]
    return json.dumps(files)


@app.route('/getGalleryImage/<filename>', methods=['GET'])
def getGalleryImage(filename):
    if os.path.exists('./gallery/'+filename):
        with open('./gallery/'+filename, 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')
    return ''


@app.route('/submitToGallery', methods=['GET', 'POST'])
def submitToGallery():
    if request.method == 'POST':
        sessionId = request.form['id']

        style_out = './output/style/'+sessionId+'.png'

        if os.path.isfile(style_out):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            shutil.copy2(style_out, './gallery/'+timestr+'.png')
            return 'True'
        else:
            return 'False'

    return 'submitToGallery'


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    print('Start serving style transfer at port 5002...')
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
