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
        print('already exists, loading')
    
    global backup
    
    backup = read_data()

    load_disabled_features(backup)
    # print("Previously disabled features: " + backup + '\n')
    


def save(new):
    print('saving')
    if new not in backup:
        backup = open(file, "w")
        backup.write(str(new))
        backup.close
    else:
        print('Feature Laready Exists in Backup')