FIRST_SLOT = (960, 300)
SECOND_SLOT = (960, 420)
THIRD_SLOT = (960, 540)

FIRST_ITEM = (750, 200)
SECOND_ITEM = (900, 200)

CHOICE_CLICK = (840, 270)
FIRST_CHOICE = (560, 270)
SECOND_CHOICE = (500, 400)
THIRD_CHOICE = (400, 470)
FOURTH_CHOICE = (300, 530)
FIFTH_CHOICE = (160, 550)

POPUP_CONFIRM = (750, 500)
CONFIRM = (1080, 640)

from os import system

def touch(point):
    x, y = point
    system(f"adb shell input tap {x} {y}")