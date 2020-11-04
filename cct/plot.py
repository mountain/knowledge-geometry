import cv2
import numpy as np

img = np.zeros([255, 255], dtype=np.int)
img[64:192, 64] = np.ones([128], dtype=np.int) * 255
img[64:192, 192] = np.ones([128], dtype=np.int) * 255
img[64, 64:192] = np.ones([128], dtype=np.int) * 255
img[192, 64:192] = np.ones([128], dtype=np.int) * 255
cv2.imwrite('orig.png', img)


def transform(z):
    return np.exp(z) / 6


def grid_sample(img, w):
    t1 = np.zeros(w.shape, dtype=np.int)
    t2 = np.zeros(w.shape, dtype=np.int)
    grid = (128 + 128j) + 128 * w

    tx = np.round(np.real(grid)).astype(np.int)
    ty = np.round(np.imag(grid)).astype(np.int)
    t1[ty, tx] = img

    tx = np.round(np.real(grid) + 0.5).astype(np.int)
    ty = np.round(np.imag(grid) + 0.5).astype(np.int)
    t2[ty, tx] = img

    return t1 + t2


def apply(img, t):
    x, y = np.meshgrid(np.linspace(-1.0, 1.0, 255), np.linspace(-1.0, 1.0, 255))
    z = x + 1j * y
    img = img + grid_sample(img, t(z))
    img = img + grid_sample(img, t(z))
    img = img + grid_sample(img, t(z))
    return img


cv2.imwrite('sample.png', apply(img, transform))










