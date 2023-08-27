import cv2 as cv
from pathlib import PurePath
from os import mkdir, listdir
from os.path import exists

MAIN_DIR = PurePath(__file__).parents[1]
COLLAGE = MAIN_DIR.joinpath("collage")
EXTRACTED_IMAGE = MAIN_DIR.joinpath("extracted_image")

if not exists(str(EXTRACTED_IMAGE)):
    mkdir(str(EXTRACTED_IMAGE))
if not exists(str(COLLAGE)):
    mkdir(str(COLLAGE))


def blur(img):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(img_rgb, tuple(37 for _ in range(2)), 8)
    return blur_img


def mask(blur_img):
    low = 105
    max_num = 255
    _, thresh = cv.threshold(blur_img, low, max_num, cv.THRESH_BINARY)
    return thresh


def contour(mask_img):
    cont, _ = cv.findContours(mask_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print(f"number of images: {len(cont)}")
    cont_image = cv.drawContours(img, cont, -1, 255, 3)
    return cont, cont_image


def show_boundingrect(cont, cont_image):
    for c in cont:
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(cont_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    resize_sample_image = cv.resize(
        cont_image, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR
    )
    cv.imshow("with bounding boxes", resize_sample_image)
    cv.waitKey()


def save_images(cont, image_subfolder: str):
    save_subfolder = str(EXTRACTED_IMAGE.joinpath(image_subfolder))
    if not exists(save_subfolder):
        mkdir(save_subfolder)
    idx = [int(x[:-4]) for x in listdir(save_subfolder)]
    number = 0 if len(idx) == 0 else max(idx)
    for c in cont:
        number += 1
        x, y, w, h = cv.boundingRect(c)
        roi = image_to_output[y : y + h, x : x + w]
        cv.imwrite(f"{save_subfolder}/{str(number)}" + ".jpg", roi)


def main(save: bool, image_subfolder: str):
    blur_img = blur(img)
    mask_img = mask(blur_img)
    cont, cont_img = contour(mask_img)
    if not save:
        show_boundingrect(cont, cont_img)
    if save:
        save_images(cont, image_subfolder)
        show_boundingrect(cont, cont_img)


if __name__ == "__main__":
    entry = input("Image name: ")
    files = listdir(COLLAGE)
    image_entry = next(file for file in files if entry.lower() in file.lower())
    image = str(COLLAGE.joinpath(image_entry))
    print(image)
    cv_img = cv.imread(image)
    img = cv.rotate(cv_img.copy(), cv.ROTATE_90_CLOCKWISE)
    image_to_output = cv.rotate(cv_img, cv.ROTATE_90_CLOCKWISE)
    main(True, image_entry[:-4])
