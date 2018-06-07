from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import json
import base64
import io

from PIL import Image


def pix_translate(input_file, output_file, model_dir='models/pix2pix'):
    with open(input_file, "rb") as f:
        im = Image.open(input_file)
        im = im.resize((256, 256), Image.ANTIALIAS)
        imByteArr = io.BytesIO()
        im.save(imByteArr, format='PNG')
        input_data = imByteArr.getvalue()
        # input_data = f.read()

    input_instance = dict(input=base64.urlsafe_b64encode(
        input_data).decode("ascii"), key="0")
    input_instance = json.loads(json.dumps(input_instance))

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(model_dir + "/export.meta")
        saver.restore(sess, model_dir + "/export")
        input_vars = json.loads(tf.get_collection("inputs")[0].decode("utf-8"))
        output_vars = json.loads(tf.get_collection("outputs")[0].decode("utf-8"))
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(
            output_vars["output"])

        input_value = np.array(input_instance["input"])
        output_value = sess.run(
            output, feed_dict={input: np.expand_dims(input_value, axis=0)})[0]

    output_instance = dict(output=output_value.decode("ascii"), key="0")

    b64data = output_instance["output"]
    b64data += "=" * (-len(b64data) % 4)
    output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))

    with open(output_file, "wb") as f:
        f.write(output_data)

    return True


def main():
    print(pix_translate('uploads/_3ptklqgx9.png', '5.2.png'))


if __name__ == '__main__':
    main()
