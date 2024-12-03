# Wordle Database Management System: Internal Documentation

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Introduction](#1-introduction)
* [2. Database Schema](#2-database-schema)
* [3. Module Functions](#3-module-functions)
    * [3.1. `open()`](#31-open)
    * [3.2. `close()`](#32-close)
    * [3.3. `do()`](#33-do)
    * [3.4. `make_table()`](#34-make_table)
    * [3.5. `add_words()`](#35-add_words)
    * [3.6. `get_words()`](#36-get_words)
    * [3.7. `get_player()`](#37-get_player)
    * [3.8. `make_database()`](#38-make_database)
    * [3.9. `add_player()`](#39-add_player)
    * [3.10. `get_leaderboard()`](#310-get_leaderboard)


## 1. Introduction

This document details the functionality of the Python module designed to manage a SQLite database for a Wordle game.  The module handles database creation, word storage, and player leaderboard management.

## 2. Database Schema

The database (`wordle.db`) contains two tables:

| Table Name     | Columns                                      | Description                                                                     |
|-----------------|----------------------------------------------|---------------------------------------------------------------------------------|
| `wordle`        | `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `words` (VARCHAR) | Stores the Wordle words. `id` is an auto-incrementing unique identifier for each word. |
| `leaderboard`   | `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `name` (VARCHAR), `attempts` (INTEGER), `word_id` (INTEGER, FOREIGN KEY referencing `wordle`.`id`) | Stores player scores, linking player attempts to specific Wordle words.       |


## 3. Module Functions

### 3.1. `open()`

Establishes a connection to the SQLite database and creates a cursor object.  Handles global variables `conn` and `cursor` for database connection and cursor respectively.

```python
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
```

### 3.2. `close()`

Closes the database cursor and connection, releasing resources.

```python
def close():
    cursor.close()
    conn.close()
```

### 3.3. `do()`

Executes a given SQL query and commits the changes to the database. This function simplifies database interactions.

```python
def do(query):
    cursor.execute(query)
    conn.commit()
```

### 3.4. `make_table()`

Creates the `wordle` and `leaderboard` tables in the database if they don't exist.  It ensures foreign key constraints are enabled.

```python
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
```

### 3.5. `add_words()`

Adds a list of words to the `wordle` table. Uses `executemany` for efficient insertion of multiple rows.

```python
def add_words():
    open()
    words = [('hamburger',),
             ('pizza',),
             ('audio',),
             ('playstation',)]
    cursor.executemany('INSERT INTO wordle (words) VALUES (?)', words)
    conn.commit()
    close()
```

### 3.6. `get_words()`

Retrieves all words from the `wordle` table. Returns a list of tuples, where each tuple represents a word.

```python
def get_words():
    open()
    cursor.execute('SELECT * FROM wordle')
    wordle_data = cursor.fetchall()
    close()
    return wordle_data
```

### 3.7. `get_player()`

Retrieves all player data from the `leaderboard` table. Returns a list of tuples, each representing a player's record.

```python
def get_player():
    open()
    cursor.execute('SELECT * FROM leaderboard')
    leaderboard_data = cursor.fetchall()
    close()
    return leaderboard_data
```

### 3.8. `make_database()`

A convenience function that creates the database tables and adds initial words.

```python
def make_database():
    make_table()
    add_words()
```

### 3.9. `add_player()`

Adds a new player's score to the `leaderboard` table. Prints a confirmation message.

```python
def add_player(name, attempts, word_id):
    open()
    cursor.execute("INSERT INTO leaderboard (name, attempts, word_id) VALUES (?, ?, ?)", (name, attempts, word_id))
    conn.commit()
    print(f"The player: {name}, takes {attempts} attempts to finish this word with id {word_id}")
    close()
```

### 3.10. `get_leaderboard()`

Retrieves the leaderboard for a specific word, sorted by attempts.

```python
def get_leaderboard(word_id):
    open()
    command = f"SELECT * FROM leaderboard WHERE word_id = {word_id} ORDER BY attempts ASC"
    cursor.execute(command)
    leaderboard = cursor.fetchall()
    close()
    return leaderboard
```
