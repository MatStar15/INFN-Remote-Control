import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()


def debug_populate_db(): #TODO: Remove this function
    cur.execute("DELETE FROM data")

    records = [(r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/flaskr/static/IMG/IMG1.jpg',
                r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/text_data/test.txt'),
            (r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/flaskr/static/IMG/IMG2.jpg',
                r'C:/Users/user/CLionProjects/sorting/INFN Remote Control/text_data/test2.txt')
    ]
    # populate with test use raw string to avoid formatting etc.
    cur.executemany("INSERT INTO data (img_path, root_path) VALUES (?,?);", records) # EXECUTE ****MANY****
    con.commit()


def create_db():


    cur.execute("""
                
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    
                    img_path TEXT,
                    root_path TEXT,
                    name TEXT
                )            
                """)
    con.commit()

    debug_populate_db() #TODO: Remove this function

def db_insert(record):
    try:
        cur.execute("INSERT INTO data (img_path, root_path) VALUES(?,?)", record)
        con.commit()
        print("INSERT SUCCESSFUL")
    except:
        print("INSERT FAILED")

def db_select():
    res = cur.execute("SELECT (id, date, img_path, root_path) FROM data") #TODO pass ID as get parameter in the link, so that it can be used to set the name of the record
    return res.fetchall()