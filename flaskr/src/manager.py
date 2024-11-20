# import machineScripts as ms
from time import sleep
from . import events

test_images = [ 'IMG1.jpg', 'IMG2.jpg'] #TODO: implement actual database query to get the images
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


# database interface
from .db_manager import *

# def get_file_path(file_id: int):
#     return db_get_file_path(file_id)

# def get_all_folders():
#     return db_get_all_folders()

# def get_folder_name(folder_id: int):
#     return db_get_folder_name(folder_id)




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

#TODO implement function to scrape the folder for files and images
    #TODO: get folder from user input (maybe add foldesr to the database, different  table and reference it in the data table. So that you can select entries in a specific folder)
    #TODO: function that gets all the files from the folder and inserts them in the database
    #NOTE that there has to be a seprate function for adding to the database
    #TODO: function that when the machine is running checks for a new file and adds it to the database
        #TODO: function that calls the renderer to genereate the new image when it is not already available for the file.
        #NOTE this fuction has to be called when the files is requested by the user.
    
#NOTE the data file name is unknown, so have to constantly look for new files in the folder (maybe it is known after the first file of the session is added to the database)
    
#TODO: ceate a class for the machine that has the following methods: status (dictionary with working folder, if known the session name, and the current file name).
    

#NOTE maybe add groups to file ntries in the database, so that the user can select a group of files coming from the same run, (file name should be similar if they are from the same run)