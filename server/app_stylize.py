from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# coding=utf-8

# import pix2pix as pix
import stylize

import os
import base64
import json
import re
from io import BytesIO
from PIL import Image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, Response, send_file, make_response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    # Main page

    return 'style server running'

    with open(os.path.join(os.path.dirname(__file__), 'styles/1.jpg'), 'rb') as f:
        return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')
    

@app.route('/getStyleFromId', methods=['GET', 'POST'])
def getPix():
    if request.method == 'POST':
        sessionId = request.form['id']
        styleId = request.form['style']
        # imgBase64 = request.form['image']
        # image_data = re.sub('^data:image/.+;base64,', '', imgBase64)
        # image = Image.open(BytesIO(base64.b64decode(image_data)))

        # basepath = os.path.dirname(__file__)
        # file_path = os.path.join(
        #     basepath, 'uploads', '{}.png'.format(sessionId))
        # image.save(file_path)

        pix_out = './output/pix/'+sessionId+'.png'
        style_out = './output/style/'+sessionId+'.png'
        # pix.pix_translate(input_file=file_path, output_file=pix_out)
        stylize.get_stylize_image(pix_out, './styles/'+styleId+'.jpg', style_out)
        # print(pix_out)
        with open(os.path.join(os.path.dirname(__file__), style_out), 'rb') as f:
            return u"data:image/png;base64," + base64.b64encode(f.read()).decode('ascii')

    return 'invalid request'


if __name__ == '__main__':
    # app.run(port=5000, debug=True)

    # st.get_style_image(content='sometest/1.jpg', style='styles/impronte_d_artista.jpg')

    # Serve the app with gevent
    print('Start serving style transfer...')
    http_server = WSGIServer(('', 5002), app)
    http_server.serve_forever()
    print('Service started at port 5000')
