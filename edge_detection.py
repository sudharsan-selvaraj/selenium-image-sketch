from utils import imread, imsave
import numpy as np
from scipy.ndimage.filters import convolve, gaussian_filter
import potrace


def canny_edge_detector(im, blur=2, Threshold=50):
    im = np.array(im, dtype=float)
    im2 = gaussian_filter(im, blur)
    im3h = convolve(im, [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    im3v = convolve(im, [[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    grad = np.power(np.power(im3h, 2.0) + np.power(im3v, 2.0), 0.5)
    theta = np.arctan2(im3v, im3h)
    thetaQ = (np.round(theta * (5.0 / np.pi)) + 5) % 5
    gradSup = grad.copy()
    for r in range(im.shape[0]):
        for c in range(im.shape[1]):
            if r == 0 or r == im.shape[0] - 1 or c == 0 or c == im.shape[1] - 1:
                gradSup[r, c] = 0
                continue
            tq = thetaQ[r, c] % 4
            if tq == 0:
                if grad[r, c] <= grad[r, c - 1] or grad[r, c] <= grad[r, c + 1]:
                    gradSup[r, c] = 0
            if tq == 1:
                if grad[r, c] <= grad[r - 1, c + 1] or grad[r, c] <= grad[r + 1, c - 1]:
                    gradSup[r, c] = 0
            if tq == 2:
                if grad[r, c] <= grad[r - 1, c] or grad[r, c] <= grad[r + 1, c]:
                    gradSup[r, c] = 0
            if tq == 3:
                if grad[r, c] <= grad[r - 1, c - 1] or grad[r, c] <= grad[r + 1, c + 1]:
                    gradSup[r, c] = 0

    return gradSup > Threshold


def get_edge_detected_image(image_path = None):
    gray = imread(image_path, False, 'L')
    gray = canny_edge_detector(gray)
    # imsave('sobel_converted.png', gray / np.amax(gray))
    return gray / np.amax(gray)


def get_image_cuve_paths(image_path = None):
    im = get_edge_detected_image(image_path)
    bmp = potrace.Bitmap(im)
    return bmp.trace(alphamax=0)


