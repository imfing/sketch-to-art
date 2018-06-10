from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# coding=utf-8

import pix2pix as pix

import os
import base64
import json
import re
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
    return 'pix2pix server running'


@app.route('/pix-translate-data', methods=['GET', 'POST'])
def pix_translate_data():
    if request.method == 'POST':
        sessionId = request.form['id']
        imgBase64 = request.form['image']
        image_data = re.sub('^data:image/.+;base64,', '', imgBase64)
        image = Image.open(BytesIO(base64.b64decode(image_data)))

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', '{}.png'.format(sessionId))
        image.save(file_path)

        pix_out = 'output/pix/'+sessionId+'.png'
        pix.pix_translate(input_file=file_path, output_file=pix_out)

        with open(os.path.join(os.path.dirname(__file__), pix_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return ''


if __name__ == '__main__':
    # app.run(port=5000, debug=True)

    # Serve the app with gevent
    print('Start serving pix2pix at port 5001...')
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
