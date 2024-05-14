import cv2 as cv
from cv2 import UMat
from pathlib import PurePath, Path
from typing import Sequence

MAIN_DIR = PurePath(__file__).parent
COLLAGE = MAIN_DIR.joinpath("collage")
EXTRACTED_IMAGE = MAIN_DIR.joinpath("extracted_image")

if not Path(EXTRACTED_IMAGE).exists():
    Path(EXTRACTED_IMAGE).mkdir()
if not Path(COLLAGE).exists():
    Path(COLLAGE).mkdir()


def blur(img) -> UMat:
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(
        src=img_rgb, ksize=tuple(37 for _ in range(2)), sigmaX=8)
    return blur_img


def mask(blur_img, low: int, max_num: int) -> UMat:
    _, thresh = cv.threshold(blur_img, low, max_num, cv.THRESH_BINARY)
    return thresh


def contour(mask_img: UMat, img: UMat) -> tuple[Sequence[UMat], UMat, int]:
    cont, _ = cv.findContours(mask_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print(f"number of images: {len(cont)}")
    cont_image = cv.drawContours(
        image=img, contours=cont, contourIdx=-1, color=255, thickness=3)
    return cont, cont_image, len(cont)


def show_boundingrect(cont: Sequence[UMat], cont_image: UMat):
    for c in cont:
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(cont_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    resize_sample_image = cv.resize(
        cont_image, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR
    )
    cv.imshow("with bounding boxes", resize_sample_image)
    cv.waitKey()


def save_images(cont: Sequence[UMat], image_subfolder: str, image_to_output: UMat):
    save_subfolder = EXTRACTED_IMAGE.joinpath(image_subfolder)
    if not Path(save_subfolder).exists():
        Path(save_subfolder).mkdir()
    idx = [int(file.stem) for file in Path(save_subfolder).iterdir()]
    number = 0 if len(idx) == 0 else max(idx)
    for c in cont:
        number += 1
        x, y, w, h = cv.boundingRect(c)
        roi = image_to_output[y: y + h, x: x + w]
        cv.imwrite(f"{save_subfolder}/{str(number)}" + ".jpg", roi)


def main(test: bool, image_subfolder: str, image_path: str):
    cv_img = cv.imread(image_path)
    img = cv.rotate(cv_img.copy(), cv.ROTATE_90_CLOCKWISE)
    image_to_output = cv.rotate(cv_img, cv.ROTATE_90_CLOCKWISE)
    blur_img = blur(img)
    mask_img = mask(blur_img, 105, 255)
    cont, cont_img, _ = contour(mask_img, img)
    if not test:
        show_boundingrect(cont, cont_img)
    save_images(cont, image_subfolder, image_to_output)


def cli():
    entry = input("Image name: ")
    files = Path(COLLAGE).iterdir()
    image_entry = next(
        file for file in files if entry.lower() in file.stem)
    image_path = str(COLLAGE.joinpath(image_entry))
    print(image_path)
    main(False, image_entry.stem, image_path)


if __name__ == "__main__":
    cli()
