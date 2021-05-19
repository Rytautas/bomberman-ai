import cv2
import numpy as np
import win32con
import win32gui
import win32ui

# player color in RGB
PLAYER_COLOR_LOW_RANGE = np.array([46, 79, 160])
PLAYER_COLOR_HIGH_RANGE = np.array([132, 193, 255])
DEFAULT_GAME_SCREEN_IMAGE = (480, 190, 1170, 790)


def grab_screen_img(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        left, top, x2, y2 = DEFAULT_GAME_SCREEN_IMAGE
        width = x2 - left + 1
        height = y2 - top + 1

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def process_screen_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    # get player color
    mask = cv2.inRange(original_img, PLAYER_COLOR_LOW_RANGE, PLAYER_COLOR_HIGH_RANGE)
    result = cv2.bitwise_and(original_img, original_img, mask=mask)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # add player color to character outline
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)
    processed_img = cv2.bitwise_or(processed_img, result)
    return processed_img


def display_screen_img():
    while True:
        # screen = np.array(ImageGrab.grab(bbox=(480, 190, 1170, 790)))
        screen = grab_screen_img((480, 190, 1170, 790))
        processed_screen = process_screen_img(screen)
        resized_screen = cv2.resize(processed_screen, (80, 60))
        cv2.imshow('color view', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        cv2.imshow('grayscale', processed_screen)
        cv2.imshow('resized', resized_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
