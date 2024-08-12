FIRST_SLOT = (960, 300)
SECOND_SLOT = (960, 420)
THIRD_SLOT = (960, 540)
SLOT_CONFIRM = (1080, 620)

CHOICE_CLICK = (840, 270)

FIRST_CHOICE = (560, 270)
SECOND_CHOICE = (500, 400)
THIRD_CHOICE = (400, 470)
FOURTH_CHOICE = (300, 530)
FIFTH_CHOICE = (160, 550)
CHOICE_CONFIRM = (1080, 650)

POPUP_CONFIRM = (750, 500)

from os import system

def touch(point):
    x, y = point
    system(f"adb shell input tap {x} {y}")