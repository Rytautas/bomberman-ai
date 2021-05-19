import win32api as wapi

keyList = [0x25, 0x26, 0x27, 0x28, 0x20]


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(key):
            keys.append(key)
    return keys
