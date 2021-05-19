import time

import cv2
import numpy as np

import keypress
from alexnet import alexnet
from image import grab_screen_img, process_screen_img

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'bomberman-3-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCHS)
game_screen_region = (480, 190, 1170, 790)

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()

    while True:
        moves = [0, 0, 0, 0, 0]
        screen = grab_screen_img(region=game_screen_region)
        screen = process_screen_img(screen)
        screen = cv2.resize(screen, (80, 60))

        print("Frame took {} seconds".format(time.time() - last_time))
        last_time = time.time()

        prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 3)])[0]
        argmax = np.argmax(list(prediction))
        moves[argmax] = 1
        print(moves, prediction)

        if moves == [1, 0, 0, 0, 0]:
            keypress.left()
        elif moves == [0, 1, 0, 0, 0]:
            keypress.up()
        elif moves == [0, 0, 1, 0, 0]:
            keypress.right()
        elif moves == [0, 0, 0, 1, 0]:
            keypress.down()
        elif moves == [0, 0, 0, 0, 1]:
            keypress.bomb()


main()
