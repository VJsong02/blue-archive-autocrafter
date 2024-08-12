from os import system
import cv2
import numpy as np
from datetime import datetime
import pytesseract
from sys import stderr as err
from touch import *

def main():
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"

    main_mask = cv2.imread("./images/mainmask.png")
    main_mask = cv2.cvtColor(main_mask, cv2.COLOR_RGB2GRAY)

    confirm_mask = cv2.imread("./images/confirm1mask.png")
    confirm_mask = cv2.cvtColor(confirm_mask, cv2.COLOR_RGB2GRAY)

    while True:
        # start = datetime.now()
        system("adb exec-out screencap > screenshot.raw")

        img = None
        with open("screenshot.raw", "rb") as file:
            cols = 1280
            rows = 720
            f = np.fromfile(file, dtype=np.uint8, count=rows * cols * 4 + 16)
            img = f[16:].reshape((rows, cols, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = 255 - img
            img = cv2.bitwise_and(img, img, mask=main_mask)
            # print(pytesseract.image_to_string(cv2.bitwise_and(img, img, mask=confirm_mask)))
            print(pytesseract.image_to_string(img))
            print("-" * 150)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # print(img[0][0])
            # exit()

        cv2.imshow("shiroko", img)
        # finish = datetime.now()

        # print(f"{round(1000000 / (finish - start).microseconds, 2):.2f}", "fps", end="\r", file=err)

        cv2.waitKey(1)

if __name__ == "__main__":
    main()
