import numpy as np
from alexnet import alexnet

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'bomberman-3-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCHS)
np_load_old = np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)


def train_model():
    model = alexnet(WIDTH, HEIGHT, LR)

    train_data = np.load('training_data_v2.npy')

    train = train_data[:-500]
    test = train_data[-500:]

    X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
    Y = [i[1] for i in train]

    test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
    test_Y = [i[1] for i in test]

    model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS,
              validation_set=({'input': test_X}, {'targets': test_Y}),
              snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

    # tensorboard --logdir=D:/Programming/bomberman-ai/log
    model.save(MODEL_NAME)


train_model()
