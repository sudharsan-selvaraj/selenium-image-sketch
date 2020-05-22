from edge_detection import get_image_cuve_paths
import argparse
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import datetime

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--image', type=str)

ARGS = PARSER.parse_args()

if ARGS.image is None:
    print("Image path cannot be empty")
    sys.exit(1)


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path="/Users/sudharsan/Documents/Applications/chromedriver")
    driver.get("https://vrobbi-nodedrawing.herokuapp.com/")
    return driver


# Find the co-ordinates of the image outline after applying sobel filter
# and use Canny edge detection algorithm to find the edges from the input image.
def get_image_coordinates(input_image_path):
    print("Detecting edges from the image..")
    image_graph_path = get_image_cuve_paths(input_image_path)
    print("{}{}".format("Total no of curves found is ", len(image_graph_path.curves)))
    return image_graph_path


def draw():

    image_coordinates = get_image_coordinates(ARGS.image)

    # To avoid image from moving out of the screen, adjust the position of X and Y axis.
    # This will vary for each and every image based on its original dimension
    diffX = -300
    diffY = -10
    first = 0

    driver = get_driver()
    body_element = driver.find_element_by_tag_name("body")
    sleep(3)

    index = 1
    execution_start_time = datetime.datetime.now()

    # Loop through each curves obtained from the edge detected image
    for curve in image_coordinates:
        # skip first path, which is the border
        if first == 0:
            first = 1
            continue

        curve_start_time = datetime.datetime.now()
        start_x, start_y = curve.start_point

        actions = ActionChains(driver)
        action_chain = actions.move_to_element_with_offset(body_element, start_x - diffX, start_y - diffY) \
            .click_and_hold()

        curve_starting_point = {'x': start_x - diffX, 'y': start_y - diffY}

        for segment in curve:
            end_point_x, end_point_y = segment.end_point
            c_x, c_y = segment.c

            action_chain = action_chain.move_to_element_with_offset(body_element, c_x - diffX, c_y - diffY) \
                .move_to_element_with_offset(body_element, end_point_x - diffX, end_point_y - diffY)

        # Reconnect the end back to the stating point to complete the curve.
        action_chain.move_to_element_with_offset(body_element, curve_starting_point.get("x"),
                                                 curve_starting_point.get("y")) \
            .release().perform()

        print("{}{} in {}".format("Completed curve ", index, datetime.datetime.now() - curve_start_time))
        index = index + 1

    print("Completed in {}".format(datetime.datetime.now() - execution_start_time))

draw()
