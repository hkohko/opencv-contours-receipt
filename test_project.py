import cv2 as cv
from cv2 import UMat
from project import blur, mask, contour, save_images
from pathlib import PurePath, Path

MAIN_DIR = PurePath(__file__).parent
COLLAGE = MAIN_DIR.joinpath("collage")
EXTRACTED_IMAGE = MAIN_DIR.joinpath("extracted_image")


def open_image() -> tuple[UMat, UMat]:
    image_path = PurePath(COLLAGE).joinpath("test_image.jpg")
    assert Path(image_path).exists()
    cv_img = cv.imread(str(image_path))
    img = cv.rotate(cv_img.copy(), cv.ROTATE_90_CLOCKWISE)
    image_to_output = cv.rotate(cv_img, cv.ROTATE_90_CLOCKWISE)
    return img, image_to_output


def test_blur():
    img, _ = open_image()
    blurred = blur(img)
    assert (len(blurred.shape) == 2)


def test_mask():
    img, image_to_output = open_image()
    blurred = blur(img)
    masked = mask(blurred, 105, 255)
    cont, cont_img, num_of_image = contour(masked, img)
    # test_image.jpeg only has 4 objects of interest in it
    # blurring and masking parameters influences the number of images detected
    assert (num_of_image == 4)


def test_save_images():
    ...
