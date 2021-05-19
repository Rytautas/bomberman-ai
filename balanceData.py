import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

np_load_old = np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
train_data = np.load('resized_training_data.npy')


def check_training_data():
    for data in train_data:
        img = data[0]
        choice = data[1]
        cv2.imshow('test', img)
        print(choice)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

stands = []
lefts = []
rights = []
ups = []
downs = []
spaces = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1, 0, 0, 0, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 0, 0, 0]:
        ups.append([img, choice])
    elif choice == [0, 0, 1, 0, 0]:
        rights.append([img, choice])
    elif choice == [0, 0, 0, 1, 0]:
        downs.append([img, choice])
    elif choice == [0, 0, 0, 0, 1]:
        spaces.append([img, choice])

ups = ups[:len(lefts)][:len(stands)][:len(rights)][:len(downs)][:len(spaces)]
lefts = lefts[:len(stands)][:len(ups)][:len(rights)][:len(downs)][:len(spaces)]
rights = rights[:len(lefts)][:len(ups)][:len(stands)][:len(downs)][:len(spaces)]
downs = downs[:len(lefts)][:len(ups)][:len(rights)][:len(stands)][:len(spaces)]

final_data = stands + ups + lefts + rights + downs + spaces
shuffle(final_data)
print("training data: {}".format(len(train_data)))
print("final data: {}".format(len(final_data)))
np.save('training_data_v2.npy', final_data)
