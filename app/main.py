import cv2 as cv
from os import getcwd, mkdir, listdir
from os.path import exists

if not exists("extracted_image"):
    mkdir("extracted_image")

image = rf"{getcwd()}\multiple_imgs_2.jpg"
print(image)
assert image is not None, "image not found"
cv_img = cv.imread(image)
img = cv.rotate(cv_img.copy(), cv.ROTATE_90_CLOCKWISE)
image_to_output = cv.rotate(cv_img, cv.ROTATE_90_CLOCKWISE)


def blur(img):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(img_rgb, tuple(31 for _ in range(2)), 8)
    return blur_img


def mask(blur_img):
    low = 95
    max_num = 255
    _, thresh = cv.threshold(blur_img, low, max_num, cv.THRESH_BINARY)
    return thresh


def contour(mask_img):
    cont, _ = cv.findContours(mask_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print(f"number of images: {len(cont)}")
    cont_image = cv.drawContours(img, cont, -1, 255, 3)
    return cont, cont_image


def show_boundingrect(cont, cont_image):
    idx = [int(x[:-4]) for x in listdir(f"{getcwd()}/extracted_image")]
    number = 0 if len(idx) == 0 else max(idx)
    for c in cont:
        number += 1
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(cont_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    resize_sample_image = cv.resize(
        cont_image, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR
    )
    cv.imshow("with bounding boxes", resize_sample_image)
    cv.waitKey()


def save_images(cont):
    idx = [int(x[:-4]) for x in listdir(f"{getcwd()}/extracted_image")]
    number = 0 if len(idx) == 0 else max(idx)
    for c in cont:
        number += 1
        x, y, w, h = cv.boundingRect(c)
        roi = image_to_output[y : y + h, x : x + w]
        cv.imwrite(f"{getcwd()}/extracted_image/{str(number)}" + ".jpg", roi)


def main(save: bool):
    blur_img = blur(img)
    mask_img = mask(blur_img)
    cont, cont_img = contour(mask_img)
    show_boundingrect(cont, cont_img)
    if save:
        save_images(cont)


if __name__ == "__main__":
    main(False)
