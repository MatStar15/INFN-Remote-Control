from .manager import load_disabled_features

file = "disabled_features_backup.txt"

to_strip = '[]\''

backup = []

def read_data():
    data = []
    with open(file, 'r') as f:
        for entry in f:
            entry = entry.strip(to_strip)
            data.append(entry)
    return data

def setup():
    try: 
        open(file, "x")
    except:
        print('\nBackup file exists, loading content\n')
    
    global backup
    
    backup = read_data()

    load_disabled_features(backup)
    # print("Previously disabled features: " + backup + '\n')


def write_to_file(data):
    backup = open(file, "w")
    backup.write(str(data))
    backup.close


def save(new):
    print('saving')
    try:
        if new not in backup:
            write_to_file(new)
        else:
            print('Feature Laready Exists in Backup')
    except:
        write_to_file(new)