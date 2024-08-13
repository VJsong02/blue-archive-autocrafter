from os import system
import cv2
import numpy as np
import pytesseract
from datetime import datetime
from time import sleep
from string import ascii_letters

from touch import *

COLS = 1280
ROWS = 720


def match(img, template):
    h, w = template.shape
    res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)

    conf, _, min_loc, _ = cv2.minMaxLoc(res)

    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return top_left, bottom_right, conf / h / w < 1000


def main_screen():
    main_mask = cv2.imread("./images/mainmask.png")
    main_mask = cv2.cvtColor(main_mask, cv2.COLOR_RGB2GRAY)

    found_text = None
    while True:
        system("adb exec-out screencap > screenshot.raw")

        img = None
        with open("screenshot.raw", "rb") as file:
            f = np.fromfile(file, dtype=np.uint8, count=ROWS * COLS * 4 + 16)
            img = f[16:].reshape((ROWS, COLS, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = 255 - img
            img = cv2.bitwise_and(img, img, mask=main_mask)

            found_text = [*filter(None, pytesseract.image_to_string(img).split("\n"))]
            if "Claim All" in found_text:
                break

    match len(found_text):
        case 4:
            touch(FIRST_SLOT)
        case 3:
            touch(SECOND_SLOT)
        case 2:
            touch(THIRD_SLOT)
        case 1:
            touch(CONFIRM)
            sleep(0.3)
            touch(POPUP_CONFIRM)
            sleep(0.3)
            touch(CONFIRM)
            sleep(2)
            touch(CONFIRM)
            return 1


def item_screen():
    choice_mask = cv2.cvtColor(cv2.imread("./images/choicemask.png"), cv2.COLOR_RGB2GRAY)
    choice_mask2 = cv2.cvtColor(cv2.imread("./images/choicemask2.png"), cv2.COLOR_RGB2GRAY)
    big = 255 - cv2.cvtColor(cv2.imread("./images/big_thingies.png"), cv2.COLOR_RGB2GRAY)
    small = 255 - cv2.cvtColor(cv2.imread("./images/small_thingies.png"), cv2.COLOR_RGB2GRAY)

    while True:
        system("adb exec-out screencap > screenshot.raw")

        img = None
        with open("screenshot.raw", "rb") as file:
            f = np.fromfile(file, dtype=np.uint8, count=ROWS * COLS * 4 + 16)
            img = f[16:].reshape((ROWS, COLS, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = 255 - img

            mask2 = cv2.bitwise_and(img, img, mask=choice_mask2)
            found_text = [
                *filter(
                    None,
                    pytesseract.image_to_string(
                        mask2, config="-c tessedit_char_whitelist=0123456789x"
                    ).split(),
                )
            ]

            mask1 = cv2.bitwise_and(img, choice_mask)
            ba, bb, bconf = match(mask1, big)
            cv2.rectangle(img, ba, bb, 255, 1)
            sa, sb, sconf = match(mask1, small)
            cv2.rectangle(img, sa, sb, 255, 1)
            # print(bconf, sconf)

            if bconf:
                if sconf:
                    if ba < sa: # big one is first
                        touch(FIRST_ITEM)
                    else:
                        for _ in range(10):
                            touch(SECOND_ITEM)
                            sleep(0.1)
                else:
                    touch(FIRST_ITEM)
            elif sconf:
                for _ in range(10):
                    touch(SECOND_ITEM)
                    sleep(0.1)

            if bconf or sconf:
                touch(CONFIRM)
                return



        # end = datetime.now()
        # fps = f"{1e6 / (end - start).microseconds:.2f} fps"
        # img = cv2.bitwise_and(img, choice_mask)
        # img = cv2.putText(img, fps, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
        # cv2.imshow(
        #     "shiroko",
        #     img,
        # )
        # cv2.waitKey(1)


def node_screen():
    confirm_mask = cv2.cvtColor(cv2.imread("./images/confirm1mask.png"), cv2.COLOR_RGB2GRAY)

    touch(CHOICE_CLICK)
    sleep(0.3)
    nodes = [FIRST_CHOICE, SECOND_CHOICE, THIRD_CHOICE, FOURTH_CHOICE, FIFTH_CHOICE]

    options = []
    while True:
        # start = datetime.now()
        system("adb exec-out screencap > screenshot.raw")

        img = None
        with open("screenshot.raw", "rb") as file:
            touch(nodes[len(options)])
            system("adb exec-out screencap > screenshot.raw")

            f = np.fromfile(file, dtype=np.uint8, count=ROWS * COLS * 4 + 16)
            img = f[16:].reshape((ROWS, COLS, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            masked = cv2.bitwise_and(img, img, mask=confirm_mask)
            found_text = pytesseract.image_to_string(masked, config="--psm 7 -c tessedit_char_whitelist=" + ascii_letters).strip()
            if len(found_text) < 3:
                touch(CHOICE_CLICK)
                sleep(0.3)
                continue

            if not found_text in options:
                # print("option", len(options), "is", found_text)
                options.append((found_text, len(options)))
            if len(options) == 5:
                break
            
    def order(s):
        s = s[0]

        if "Set" in s or "Development" in s:
            return 0
        
        if "Colorful" in s:
            return 1

        if "Flower" in s:
            return 2
        
        if "Radiant" in s:
            return 3
        
        if "Shiny" in s:
            return 4
        
        return 999
    
    print(options)
    options.sort(key=order)
    touch(nodes[options[0][1]])
    # exit()
    touch(CONFIRM)
    sleep(0.2)
    touch(CONFIRM)


def confirm_screen():
    confirm_mask = cv2.cvtColor(cv2.imread("./images/confirm2mask.png"), cv2.COLOR_RGB2GRAY)

    while True:
        system("adb exec-out screencap > screenshot.raw")

        img = None
        with open("screenshot.raw", "rb") as file:

            f = np.fromfile(file, dtype=np.uint8, count=ROWS * COLS * 4 + 16)
            img = f[16:].reshape((ROWS, COLS, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            masked = cv2.bitwise_and(img, img, mask=confirm_mask)
            found_text = pytesseract.image_to_string(masked, config="--psm 7").strip()
            if found_text == "Start Crafting":
                break

    touch(CONFIRM)
    sleep(0.3)
    touch(POPUP_CONFIRM)
    touch(CONFIRM)


def main():
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"

    confirm_mask = cv2.imread("./images/confirm1mask.png")
    confirm_mask = cv2.cvtColor(confirm_mask, cv2.COLOR_RGB2GRAY)

    while True:
        if main_screen() != None:
            continue
        item_screen()
        node_screen()
        confirm_screen()
        # break

if __name__ == "__main__":
    main()
