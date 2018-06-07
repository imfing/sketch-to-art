from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# coding=utf-8

import stylize

import os
import base64
import json
import re
from io import BytesIO
from PIL import Image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, Response, send_file, make_response
from gevent.pywsgi import WSGIServer
# from flask_cors import CORS

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'style transfer server running'


@app.route('/getStyleFromId', methods=['GET', 'POST'])
def getPix():
    if request.method == 'POST':
        sessionId = request.form['id']
        styleId = request.form['style']

        pix_out = './output/pix/'+sessionId+'.png'
        style_out = './output/style/'+sessionId+'.png'

        stylize.get_stylize_image(
            pix_out, './styles/'+styleId+'.jpg', style_out)

        with open(os.path.join(os.path.dirname(__file__), style_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return 'invalid request'


if __name__ == '__main__':
    # app.run(port=5000, debug=True)

    # Serve the app with gevent
    print('Start serving style transfer at port 5002...')
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
