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


@app.route('/stylize-with-data', methods=['GET', 'POST'])
def stylize_with_data():
    if request.method == 'POST':
        print(request.form)
        sessionId = request.form['id']
        styleId = request.form['style']
        highReality = request.form['highReality']
        highQuality = request.form['highQuality']

        userContent = request.form['userContent']
        userStyle = request.form['userStyle']
        contentData = request.form['contentData']
        styleData = request.form['styleData']

        content_size, alpha, adain = get_style_params(highQuality, highReality)

        content_path = './output/pix/'+sessionId+'.png'
        style_path = './styles/'+styleId+'.jpg'
        style_out = './output/style/'+sessionId+'.png'

        if userContent == 'true':
            content_path = './uploads/'+sessionId+'.png'
            image_data = re.sub('^data:image/.+;base64,', '', contentData)
            image_content = Image.open(BytesIO(base64.b64decode(image_data)))
            image_content.save(content_path)

        if userStyle == 'true':
            style_data = re.sub('^data:image/.+;base64,', '', styleData)
            image_style = Image.open(BytesIO(base64.b64decode(image_data)))
            style_path = os.path.join(
                './uploads', '{}_style.png'.format(sessionId))
            image_style.save(style_path)

        stylize.get_stylize_image(
            content_path, style_path, style_out,
            content_size=content_size, alpha=alpha, adain=adain)

        if userStyle == 'true':
            os.remove(style_path)

        with open(os.path.join(os.path.dirname(__file__), style_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return ''


@app.route('/get-gallery-list', methods=['GET'])
def get_gallery_list():
    galleryDir = './gallery'
    files = [os.path.basename(x) for x in sorted(
        glob.glob(os.path.join(galleryDir, '*.png')), reverse=True)]
    return json.dumps(files)


@app.route('/get-gallery-image/<filename>', methods=['GET'])
def get_gallery_image(filename):
    if os.path.exists('./gallery/'+filename):
        with open('./gallery/'+filename, 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')
    return ''


@app.route('/submit-to-gallery', methods=['GET', 'POST'])
def submit_to_gallery():
    if request.method == 'POST':
        sessionId = request.form['id']

        style_out = './output/style/'+sessionId+'.png'

        if os.path.isfile(style_out):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            shutil.copy2(style_out, './gallery/'+timestr+'.png')
            return 'True'
        else:
            return 'False'

    return ''


def get_style_params(highQuality, highReality):
    adain = False
    alpha = 0.6
    content_size = 256
    if highReality == 'true':
        adain = True
        alpha = 0.8
    if highQuality == 'true':
        content_size = 512

    return content_size, alpha, adain


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    print('Start serving style transfer at port 5002...')
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
