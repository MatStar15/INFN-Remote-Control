# import machineScripts as ms
from time import sleep
from . import events

test_images = [ 'IMG1.jpg', 'IMG2.jpg']
img_index = 0


status = ""

disabled_features = []


def get_status():
    return status


def set_status(new_status):
    global status
    status = new_status

def load_disabled_features(new):
    global disabled_features
    disabled_features = new
    print("Disabled Features: " + str(disabled_features)+ '\n')

from .backup import save

def update_disabled_features(feature):
    disabled_features.append(feature)
    save(disabled_features)

def set_disabled_features(features):
    global disabled_features
    disabled_features = features
    save(disabled_features)

def get_disabled_features():
    return disabled_features

from .events import finished

def foo ():
    # ms.CustomSystem()
    print('\nInitializing Calculations...\n')
    sleep(2)
    set_disabled_features([])
    global img_index
    img_index = (img_index+1)%2
    # print('Image Index in Foo: ' + str(img_index))
    finished(img_index)

