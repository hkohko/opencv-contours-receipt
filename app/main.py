import cv2 as cv
from pathlib import Path

"""
threshold -> threshold image
use threshold image to create an ROI
imsave the image inside each ROI
"""


def show_img(matlike):
    cv.imshow("original", matlike)
    cv.waitKey()


image = image = rf"{Path(__file__).parent.parent}/Scan_above_hvs.jpg"
cv_img = cv.imread(image)
img = cv_img.copy()
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray_img, (9,9), 1)
thresh = cv.threshold(blur, 250, 255, cv.THRESH_BINARY)
show_img(thresh[1])
