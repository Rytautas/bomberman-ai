import os.path
import time

import cv2
import numpy as np

from getkeys import key_check
from image import grab_screen_img, process_screen_img

resized_filename = 'resized_training_data.npy'
game_screen_region = (480, 190, 1170, 790)


def keys_to_output(keys):
    # left, up, right, down, space
    output = [0, 0, 0, 0, 0]
    if 0x25 in keys:
        output[0] = 1
    elif 0x26 in keys:
        output[1] = 1
    elif 0x27 in keys:
        output[2] = 1
    elif 0x28 in keys:
        output[3] = 1
    elif 0x20 in keys:
        output[4] = 1
    return output


def main():
    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    while True:
        screen = grab_screen_img(game_screen_region)
        screen = process_screen_img(screen)
        resized_screen = cv2.resize(screen, (80, 60))
        keys = key_check()
        output = keys_to_output(keys)
        resized_training_data.append([resized_screen, output])

        if len(resized_training_data) % 500 == 0:
            print(len(resized_training_data))
            np.save(resized_filename, resized_training_data)


if __name__ == '__main__':
    np_load_old = np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
    if os.path.isfile(resized_filename):
        print('File exists, loading previous data!')
        resized_training_data = list(np.load(resized_filename))
    else:
        print('File does not exist, creating new file!')
        resized_training_data = []
    main()
