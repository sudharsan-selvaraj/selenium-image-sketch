# Selenium Image Sketch:

Have you ever wondered drawing any image on html canvas using selenium is possible? Yes, it's totally possible with the help of image processing.

I have used canny edge detection algorithm to extract the outline coordinates from the input image.

Algoritm courtesy: http://people.ece.cornell.edu/

# Setup:
1. Install python
2. Install the dependencies from requirement.txt
3. Downlaod chromedriver file

# How to run?:
Enter the below command in terminal:

```bash
pyhton draw.py --image /path/to/any/image
```

This will open the chrome browser ans start sketching the image provided.
