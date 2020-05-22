import numpy as np
import potrace
from scipy import misc, ndimage
import serial

ser = serial.Serial("/dev/serial0", timeout=1)  # Open named port
ser.baudrate = 38400  # Set baud rate to 38400

import numpy as np
from scipy.ndimage.filters import convolve, gaussian_filter
from scipy.misc import imread, imshow


def CannyEdgeDetector(im, blur=2, Threshold=50):
    im = np.array(im, dtype=float)  # Convert to float to prevent clipping values

    # Gaussian blur to reduce noise
    im2 = gaussian_filter(im, blur)
    # we sometimes use blur and sometimes don't
    # Use sobel filters to get horizontal and vertical gradients
    im3h = convolve(im, [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    im3v = convolve(im, [[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    # Get gradient and direction
    grad = np.power(np.power(im3h, 2.0) + np.power(im3v, 2.0), 0.5)
    theta = np.arctan2(im3v, im3h)
    thetaQ = (np.round(theta * (5.0 / np.pi)) + 5) % 5  # Quantize direction

    # Non-maximum suppression
    gradSup = grad.copy()
    for r in range(im.shape[0]):
        for c in range(im.shape[1]):
            # Suppress pixels at the image edge
            if r == 0 or r == im.shape[0] - 1 or c == 0 or c == im.shape[1] - 1:
                gradSup[r, c] = 0
                continue
            tq = thetaQ[r, c] % 4
            if tq == 0:  # 0 is E-W (horizontal)
                if grad[r, c] <= grad[r, c - 1] or grad[r, c] <= grad[r, c + 1]:
                    gradSup[r, c] = 0
            if tq == 1:  # 1 is NE-SW
                if grad[r, c] <= grad[r - 1, c + 1] or grad[r, c] <= grad[r + 1, c - 1]:
                    gradSup[r, c] = 0
            if tq == 2:  # 2 is N-S (vertical)
                if grad[r, c] <= grad[r - 1, c] or grad[r, c] <= grad[r + 1, c]:
                    gradSup[r, c] = 0
            if tq == 3:  # 3 is NW-SE
                if grad[r, c] <= grad[r - 1, c - 1] or grad[r, c] <= grad[r + 1, c + 1]:
                    gradSup[r, c] = 0

    # Single threshold
    return (gradSup > Threshold)


maxX = 9000
maxY = 7000

# Make a grayscale numpy array
gray = misc.imread("download.png", False, 'L')
gray = CannyEdgeDetector(gray)
height = gray.shape[0]
width = gray.shape[1]
scaleFactor = min(float(maxX) / width, float(maxY) / height)
misc.imsave('sobel.png', gray / np.amax(gray))
# quit()
# Create a bitmap from the array
bmp = potrace.Bitmap(gray / np.amax(gray))
# Trace the bitmap to a path
path = bmp.trace(alphamax=0)

msg = "D 0\n"
ser.write(msg)
while (ser.readline().strip("\n\r\x00") != msg.strip("\n\r")):
    ser.write(msg)

# Iterate over path curves
first = 0
for curve in path:
    # skip first path, which is the border
    if first == 0:
        first = 1
        continue
    start_x, start_y = curve.start_point
    msg = "X %d Y %d\n" % (start_x * scaleFactor, start_y * scaleFactor)
    ser.write(msg)
    while (ser.readline().strip("\n\r\x00") != msg.strip("\n\r")):
        ser.write(msg)
    msg = "D 1\n"
    ser.write(msg)
    while (ser.readline().strip("\n\r\x00") != msg.strip("\n\r")):
        ser.write(msg)
    for segment in curve:
        end_point_x, end_point_y = segment.end_point
        c_x, c_y = segment.c
        msg1 = "X %d Y %d\n" % (c_x * scaleFactor, c_y * scaleFactor)
        msg2 = "X %d Y %d\n" % (end_point_x * scaleFactor, end_point_y * scaleFactor)
        ser.write(msg1)
        while (ser.readline().strip("\n\r\x00") != msg1.strip("\n\r")):
            ser.write(msg1)
        ser.write(msg2)
        while (ser.readline().strip("\n\r\x00") != msg2.strip("\n\r")):
            ser.write(msg2)
    msg = "D 0\n"
    ser.write(msg)
    while (ser.readline().strip("\n\r\x00") != msg.strip("\n\r")):
        ser.write(msg)
msg = "X 0 Y 0\n"
ser.write(msg)
while (ser.readline().strip("\n\r\x00") != msg.strip("\n\r")):
    ser.write(msg)
ser.close()