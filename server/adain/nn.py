import tensorflow as tf

from adain.layer import upsample_nearest, vgg_preprocess


_VGG19 = [
    ('prep', 'prep',    {}),
    ('conv', 'conv1_1', {'filters': 64}),
    ('conv', 'conv1_2', {'filters': 64}),
    ('pool', 'pool1',   {}),
    ('conv', 'conv2_1', {'filters': 128}),
    ('conv', 'conv2_2', {'filters': 128}),
    ('pool', 'pool2',   {}),
    ('conv', 'conv3_1', {'filters': 256}),
    ('conv', 'conv3_2', {'filters': 256}),
    ('conv', 'conv3_3', {'filters': 256}),
    ('conv', 'conv3_4', {'filters': 256}),
    ('pool', 'pool3',   {}),
    ('conv', 'conv4_1', {'filters': 512}),
    ('conv', 'conv4_2', {'filters': 512}),
    ('conv', 'conv4_3', {'filters': 512}),
    ('conv', 'conv4_4', {'filters': 512}),
    ('pool', 'pool4',   {}),
    ('conv', 'conv5_1', {'filters': 512}),
    ('conv', 'conv5_2', {'filters': 512}),
    ('conv', 'conv5_3', {'filters': 512}),
    ('conv', 'conv5_4', {'filters': 512}),
    ('pool', 'pool5',   {})
]


_DECODER = [
    ('conv', 'conv4_1',         {'filters': 256}),
    ('upsample', 'upsample3',   {}),
    ('conv', 'conv3_4',         {'filters': 256}),
    ('conv', 'conv3_3',         {'filters': 256}),
    ('conv', 'conv3_2',         {'filters': 256}),
    ('conv', 'conv3_1',         {'filters': 128}),
    ('upsample', 'upsample2',   {}),
    ('conv', 'conv2_2',         {'filters': 128}),
    ('conv', 'conv2_1',         {'filters': 64}),
    ('upsample', 'upsample1',   {}),
    ('conv', 'conv1_2',         {'filters': 64}),
    ('conv', 'conv1_1',         {'filters': 3})
]


def build_vgg(inputs, weights,
        last_layer='conv4_1',
        data_format='channels_first'):
    definition = _truncate(_VGG19, [last_layer])
    with tf.variable_scope('vgg'):
        layers = _build_net(definition, inputs, weights,
            activation=tf.nn.relu, trainable=False, data_format=data_format)
    return layers


def vgg_layer_params(layer):
    for _, name, params in _VGG19:
        if name == layer:
            return params
    raise ValueError('Unknown layer: ' + layer)


def  build_decoder(inputs, weights, trainable,
        activation=tf.nn.relu, data_format='channels_first'):
    with tf.variable_scope('decoder'):
        layers = _build_net(_DECODER, inputs, weights,
            activation=activation, trainable=trainable, data_format=data_format)
        return layers['conv1_1']


def _build_net(definition, inputs, weights, activation, trainable, data_format):
    layer, layers = inputs, {}
    for type, name, params in definition:
        if type == 'conv':
            if data_format == 'channels_first':
                layer = tf.pad(layer, [[0,0], [0,0], [1,1], [1,1]],
                    mode='reflect')
            else:
                layer = tf.pad(layer, [[0,0], [1,1], [1,1], [0,0]],
                    mode='reflect')
            if weights: # pretrained weights provided
                W_init = tf.constant_initializer(weights[name+'_W'])
                b_init = tf.constant_initializer(weights[name+'_b'])
            else:
                W_init = tf.contrib.layers.xavier_initializer()
                b_init = tf.zeros_initializer()
            layer = tf.layers.conv2d(layer,
                name=name,
                padding='valid',
                activation=activation,
                kernel_size=3,
                kernel_initializer=W_init,
                bias_initializer=b_init,
                trainable=trainable,
                data_format=data_format,
                **params)
        elif type == 'pool':
            layer = tf.layers.max_pooling2d(layer,
                name=name, strides=2, pool_size=2,
                data_format=data_format)
        elif type == 'upsample':
            layer = upsample_nearest(layer, scale=2, data_format=data_format)
        elif type == 'prep':
            layer = vgg_preprocess(layer, data_format=data_format)
        else:
            raise ValueError('Unknown layer: %s' % type)
        layers[name] = layer
    return layers


def _truncate(definition, used_layers):
    names = [name for _, name, _ in definition]
    return definition[:max(names.index(name) for name in used_layers)+1]
