import sqlite3

db_name = 'wordle.db'
conn = None
cursor = None

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
    do('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS wordle (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       words VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS leaderboard ( 
       id INTEGER PRIMARY KEY AUTOINCREMENT, 
       name VARCHAR, 
       attempts INTEGER, 
       word_id INTEGER, 
       FOREIGN KEY (word_id) REFERENCES wordle (id))''')
    close()

def add_words():
    open()
    words = [('volcano',),
             ('audio',),
             ('hippopotomonstrosesquippedaliophobia',),
             ('hippo',),
             ('pneumonoultramicroscopicsilicovolcanoconiosis',),
             ('laptop',),
             ('orange',),
             ('planet',),
             ('jungle',),
             ('castle',),
             ('kindly',),
             ('zipper',),
             ('manual',),
             ('design',),
             ('knight',),
             ('forest',),
             ('gentle',),
             ('flower',),
             ('muscle',),
             ('banana',),
             ('beacon',),
             ('window',),
             ('ticket',),
             ('import',),
             ('canyon',),
             ('family',),
             ('update',),
             ('people',),
             ('animal',),
             ('island',),
             ('honest',),
             ('soccer',),
             ('office',),
             ('course',),
             ('bridge',),
             ('market',),
             ('jumper',),
             ('novice',),
             ('oracle',),
             ('yonder',),
             ('victor',),
             ('heaven',),
             ('garden',),
             ('impact',),
             ('quartz',),
             ('border',),
             ('planet',),
             ('eagerly',),
             ('author',),
             ('amount',),
             ('notion',),
             ('dancer',),
             ('guity',)]
        
    cursor.executemany('INSERT INTO wordle (words) VALUES (?)', words)
    conn.commit()
    close()

def get_words():
    open()
    cursor.execute('SELECT * FROM wordle')
    wordle_data = cursor.fetchall()
    close()
    return wordle_data


def get_player():
    open()
    cursor.execute('SELECT * FROM leaderboard')
    leaderboard_data = cursor.fetchall()
    close()
    return leaderboard_data

def make_datebase():
    make_table()
    add_words()

def add_player(name, attemps, word_id):
    open()
    cursor.execute("INSERT INTO leaderboard (name, attempts, word_id) VALUES (?,?,?)", (name, attemps, word_id))
    print(f"The player: {name}, takes {attemps} attemps to finish this {word_id} word")
    close()
