import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()


def debug_populate_db(): #TODO: Remove this function
    cur.execute("DELETE FROM data")

    
    cur.execute("INSERT INTO folders(folder_path, folder_name) VALUES(?,?)", (r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/text_data/', "text_data"))
    con.commit()

    folder_id = db_get_folder_id("text_data")


    records = [(r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/flaskr/static/IMG/IMG1.jpg', folder_id, r'test.txt'),
            (r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/flaskr/static/IMG/IMG2.jpg',folder_id, r'test2.txt')]



    # populate with test use raw string to avoid formatting etc.
    cur.executemany("INSERT INTO data (img_path, folder_id, root_name) VALUES (?, ?, ?)", records) # EXECUTE ****MANY****

    con.commit()


def create_db():


    cur.execute("""
                
                CREATE TABLE IF NOT EXISTS folders(
                    folder_id INTEGER PRIMARY KEY,
                    folder_path TEXT,
                    folder_name TEXT
                )

                """) #TODO: implement use of this table

    cur.execute("""
                
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    
                    img_path TEXT,
                    folder_id INTEGER,
                    root_name TEXT,
                    CONSTRAINT fk_folders
                        FOREIGN KEY (folder_id)
                        REFERENCES folders (folder_id)
                )            
                """) 
    con.commit()

    debug_populate_db() #TODO: Remove this function



def db_get_folder_id(folder_name: str):
    res = cur.execute("SELECT folder_id FROM folders WHERE folder_name = ?", (folder_name,))
    res, = res.fetchone()
    return res
def db_get_folder_name(folder_id: int):
    res = cur.execute("SELECT folder_name FROM folders WHERE folder_id = ?", (folder_id,))
    res, = res.fetchone()
    return res

def db_get_all_folders():
    res = cur.execute("SELECT folder_name FROM folders")
    return res.fetchall()

def db_get_file_path(file_id: int):
    folder_id, = cur.execute("SELECT FROM data (folder_id) WHERE file_id = ?", file_id).fetchone
    folder_path = cur.execute("SELECT FROM folders (folder_path) WHERE folder_id = ?", folder_id).fetchone
    file_name, = cur.execute("SELECT FROM data(root_name) WHERE file_id = ?", file_id).fetchone

    return folder_path + file_name


def db_insert(record):
    try:
        cur.execute("INSERT INTO data (img_path, root_path) VALUES(?,?)", record)
        con.commit()
        print("INSERT SUCCESSFUL")
    except:
        print("INSERT FAILED")


def db_get_all_from_folder(folder_name: str):
    folder_id = db_get_folder_id(folder_name)
    res = cur.execute("SELECT (id, date, img_path, root_path) FROM data WHERE folder_id = ?", folder_id) #TODO pass ID as get parameter in the link so that it can be shared easily
    return res.fetchall()