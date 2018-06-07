import numpy as np


def coral(src, dst):
    "Correlation Alignment"
    src_flat = src.reshape(-1, 3)
    src_flat_mean = np.mean(src_flat, 0, keepdims=True)
    src_flat_std = np.std(src_flat, 0, keepdims=True)
    src_flat_norm = (src_flat - src_flat_mean) / src_flat_std
    src_flat_cov_eye = np.matmul(src_flat_norm.T, src_flat_norm) + np.eye(3)

    dst_flat = dst.reshape(-1, 3)
    dst_flat_mean = np.mean(dst_flat, 0, keepdims=True)
    dst_flat_std = np.std(dst_flat, 0, keepdims=True)
    dst_flat_norm = (dst_flat - dst_flat_mean) / dst_flat_std
    dst_flat_cov_eye = np.matmul(dst_flat_norm.T, dst_flat_norm) + np.eye(3)

    src_flat_norm_transfer = np.matmul(src_flat_norm, np.matmul(
        np.linalg.inv(_mat_sqrt(src_flat_cov_eye)),
        _mat_sqrt(dst_flat_cov_eye)
    ))
    src_flat_transfer = src_flat_norm_transfer * dst_flat_std + dst_flat_mean
    return src_flat_transfer.reshape(src.shape)


def _mat_sqrt(m):
    u, s, v = np.linalg.svd(m)
    return np.matmul(np.matmul(u, np.diag(np.sqrt(s))), v)
