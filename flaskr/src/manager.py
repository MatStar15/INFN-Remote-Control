import machineScripts as ms
from time import sleep
import src.events as events

test_value = {
    'slidebar1': 20,
    'slidebar2': 0
}

test_images = [ 'IMG1.jpg', 'IMG2.jpg']
img_index = 0


status = ""

disabled_features = []

def get_status():
    return status

def set_status(new_status):
    status = new_status

def foo ():
    # ms.CustomSystem()
    print('I am calculating...')
    sleep(2)
    global img_index
    events.update_picture(test_images[img_index])
    img_index = (img_index+1)%2

