import tensorflow as tf


def adain(content, style, epsilon=1e-5, data_format='channels_first'):
    axes = [2,3] if data_format == 'channels_first' else [1,2]

    c_mean, c_var = tf.nn.moments(content, axes=axes, keep_dims=True)
    s_mean, s_var = tf.nn.moments(style, axes=axes, keep_dims=True)
    c_std, s_std = tf.sqrt(c_var + epsilon), tf.sqrt(s_var + epsilon)

    return s_std * (content - c_mean) / c_std + s_mean
