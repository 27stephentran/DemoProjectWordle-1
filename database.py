import sqlite3
db_name = 'wordle.db'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def make_table():
    open()
    do('''PRAGMA foriegn_key=on''')
    do('''
    CREATE TABLE IF NOT EXIST wordle (
        id INTERGER PRIMARY KEY,
        words VARCHAR)''')
    
    do('''
    CREATE TABLE IF NOT EXIST leaderboard (
        id INTERGER PRIMARY KEY,
        words VARCHAR,
        attemps INTERGER,
        word_id INTERGER,
        FORIEGN KEY (word_id) REFERENCES wordle (id))''')
    close()

def add_words():
    open()
    words = [('volcano',),
             ('audio',),
             ('hippopotomonstrosesquippedaliophobia',),
             ('hippo',),
             ('pneumonoultramicroscopicsilicovolcanoconiosis',),
             ]
             
    
    cursor.executemany('INSERT INTO worlde (words) VALUE (?)', words)
    conn.commit()
    close()
