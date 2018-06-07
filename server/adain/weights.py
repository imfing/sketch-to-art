from contextlib import contextmanager

import h5py
import numpy as np


@contextmanager
def open_weights(filename):
    f = h5py.File(filename, 'r')
    yield _WeightsLoader(f)
    f.close()


class _WeightsLoader:

    def __init__(self, f):
        self._f = f


    def __getitem__(self, name):
        return np.array(self._f[name])
