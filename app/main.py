import cv2 as cv
from os import getcwd, mkdir, listdir
from os.path import exists

if not exists("extracted_image"):
    mkdir("extracted_image")

image = rf"{getcwd()}\multiple_imgs_2.jpg"
print(image)
assert image is not None, "image not found"

"""
Add gaussian blur to get rid of unnecessary edges
"""

cv_img = cv.imread(image)
cv_img_rotated = cv.rotate(cv_img, cv.ROTATE_90_CLOCKWISE)
img = cv.rotate(cv_img.copy(), cv.ROTATE_90_CLOCKWISE)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
blur = cv.GaussianBlur(img_rgb, tuple(31 for _ in range(2)), 8)  # get rid of unnecessary edges
# plt.imshow(blur)

"""
Create a mask
"""

low = 95
max_num = 255
lower_thresh = tuple(low for _ in range(3))
max_thresh = tuple(max_num for _ in range(3))
thresh = cv.inRange(blur, lower_thresh, max_thresh)
# plt.imshow(thresh, "gray")

"""
find the contours
"""

cont, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
print(f"number of images: {len(cont)}")  # this should match the number of receipts on the scanner
cont_image = cv.drawContours(img, cont, -1, 255, 3)
# plt.imshow(cont_image, "gray")

"""
create a bounding box for each contours, and extract image inside that bounding box
"""

def save_images():
    idx = [int(x[:-4]) for x in listdir(f"{getcwd()}/extracted_image")]
    number = max(idx)
    for c in cont:
        number += 1
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(cont_image,(x,y), (x+w,y+h), (0,255,0), 2)
        roi=cv_img_rotated[y:y+h,x:x+w]
        cv.imwrite(f"{getcwd()}/extracted_image/{str(number)}" + '.jpg', roi)
if __name__ == "__main__":
    save_images()
# cv.imshow('All contours with bounding box', cont_image)
# cv.waitKey(0)