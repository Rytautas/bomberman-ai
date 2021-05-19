import pyautogui


def up():
    pyautogui.keyDown('up')
    pyautogui.keyUp('down')
    pyautogui.keyUp('left')
    pyautogui.keyUp('right')


def down():
    pyautogui.keyUp('up')
    pyautogui.keyDown('down')
    pyautogui.keyUp('left')
    pyautogui.keyUp('right')


def left():
    pyautogui.keyUp('up')
    pyautogui.keyUp('down')
    pyautogui.keyDown('left')
    pyautogui.keyUp('right')


def right():
    pyautogui.keyUp('up')
    pyautogui.keyUp('down')
    pyautogui.keyUp('left')
    pyautogui.keyDown('right')


def stand():
    pyautogui.keyUp('up')
    pyautogui.keyUp('down')
    pyautogui.keyUp('left')
    pyautogui.keyUp('right')


def bomb():
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')
