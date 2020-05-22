import numpy as np
import potrace
import json
from scipy import misc, ndimage
import cv2 as cv
from time import sleep

# import serial
#
# ser = serial.Serial("/dev/serial0", timeout=1)  # Open named port
# ser.baudrate = 38400  # Set baud rate to 38400

import numpy as np
from scipy.ndimage.filters import convolve, gaussian_filter
from utils import imread, imsave
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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
gray = imread("bazinga.png", False, 'L')
gray = CannyEdgeDetector(gray)
# height = gray.shape[0]
# width = gray.shape[1]
scaleFactor = 1 #min(float(maxX) / width, float(maxY) / height)
imsave('sobel.png', gray / np.amax(gray))


im = cv.imread('sobel.png')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Create a bitmap from the array
bmp = potrace.Bitmap(gray / np.amax(gray))
# Trace the bitmap to a path
path = bmp.trace(alphamax=0)
# Iterate over path curves
first = 0
jsonDict = []

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options, executable_path ="/Users/sudharsan/Documents/Applications/chromedriver")
driver.get("https://vrobbi-nodedrawing.herokuapp.com/")
body_element = driver.find_element_by_tag_name("body")

diffX = -100
diffY = 0
sleep(3)
for curve in path:
    # skip first path, which is the border
    if first == 0:
        first = 1
        continue
    innerjson = []
    start_x, start_y = curve.start_point
    actions = ActionChains(driver)
    actions = actions.move_to_element_with_offset(body_element, start_x - diffX, start_y - diffY)\
    .click_and_hold()
    msg = "Curve X %d Y %d\n" % (start_x * scaleFactor, start_y * scaleFactor)
    print(msg)
    innerjson.append({'x':start_x * scaleFactor, 'y': start_y * scaleFactor })
    last = {'x':start_x  - diffX, 'y': start_y - diffY }
    for segment in curve:
        end_point_x, end_point_y = segment.end_point
        c_x, c_y = segment.c
        msg1 = "X %d Y %d\n" % (c_x * scaleFactor, c_y * scaleFactor)
        msg2 = "X %d Y %d\n" % (end_point_x * scaleFactor, end_point_y * scaleFactor)

        innerjson.append({'x':c_x * scaleFactor, 'y': c_y * scaleFactor })
        innerjson.append({'x':end_point_x * scaleFactor, 'y': end_point_y * scaleFactor })
        actions = actions.move_to_element_with_offset(body_element, c_x - diffX, c_y - diffY)\
            .move_to_element_with_offset(body_element, end_point_x - diffX,  end_point_y - diffY)
        print(msg1)
        print(msg2)
    innerjson.append(last)
    jsonDict.append(innerjson)
    actions.move_to_element_with_offset(body_element, last.get("x"), last.get("y")).release().perform()

jsonFile = json.dumps(jsonDict)
f = open("dict.json","w")
f.write(jsonFile)
f.close()