# Wordle Game Code Documentation

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Introduction](#1-introduction)
* [2. Modules and Imports](#2-modules-and-imports)
* [3. Global Variables](#3-global-variables)
* [4. Function: `choose_word()`](#4-function-choose_word)
* [5. Flask Application Setup](#5-flask-application-setup)
* [6. Route: `/`](#6-route-)
* [7. Route: `/wordle_page`](#7-route-wordle_page)
* [8. Function: `check_guess()`](#8-function-check_guess)
* [9. Application Execution](#9-application-execution)


## 1. Introduction

This document provides internal code documentation for the Wordle game implemented using Flask.  The game allows users to guess a randomly selected word within a set number of attempts.  The application uses a database to store words and player scores.

## 2. Modules and Imports

The application utilizes several modules:

* `flask`: Provides the web framework for creating the application.
* `random`: Used for randomly selecting a word from the database.
* `database`: A custom module (presumably containing database interaction functions).
* `os`: Used for checking the existence of the database file.


## 3. Global Variables

The following global variables are used:

| Variable Name  | Data Type      | Description                                                              |
|-----------------|-----------------|--------------------------------------------------------------------------|
| `leaderboard`   | List            | Stores the leaderboard data.                                              |
| `attempts`      | Integer         | Tracks the number of attempts made by the current player.                |
| `secret_word`   | String          | Stores the randomly chosen secret word for the current game.            |
| `WORDS`         | List of tuples | Contains words retrieved from the database (each tuple: (word_id, word)).|


## 4. Function: `choose_word()`

This function selects a random word from the database and sets the `secret_word` global variable.

```python
def choose_word():
    global WORDS
    chosen_word = choice(WORDS) 
    word_id = chosen_word[0]
    secret_word = chosen_word[1].upper()
    return word_id, secret_word
```

**Algorithm:**
1. A word is randomly chosen from the `WORDS` list using `random.choice()`.
2. The word's ID (`word_id`) and the word itself (`secret_word`) are extracted from the chosen tuple.
3. The word is converted to uppercase.
4. The `word_id` and `secret_word` are returned.

## 5. Flask Application Setup

A Flask application instance is created:

```python
app = Flask(__name__)
```

## 6. Route: `/`

This route renders the main index page:

```python
@app.route("/")
def index():
    return render_template("index.html")
```

## 7. Route: `/wordle_page`

This route handles the Wordle game logic.  It processes user input, checks the guess against the secret word, and updates the game state.

```python
@app.route("/wordle_page", methods=["GET", "POST"])
def wordle_page():
    # ... (Global variable declarations and handling omitted for brevity) ...
    if request.method == "POST":
        # ... (Input processing omitted for brevity) ...

        if len(guess_word) != len(secret_word):
            # ... (Error handling omitted for brevity) ...

        feedback = check_guess(guess_word, secret_word)

        if guess_word == secret_word:
            # ... (Success handling, database update, and leaderboard update omitted for brevity) ...

        # ... (Return render_template with feedback) ...
    # ... (GET request handling and render_template omitted for brevity) ...

```

The route handles both GET and POST requests.  POST requests process user guesses.  It checks the length of the guessed word and calls the `check_guess()` function.  If the guess is correct, it updates the database, retrieves the updated leaderboard, and renders the success template. Otherwise, it provides feedback using `check_guess()` and rerenders the game page.


## 8. Function: `check_guess()`

This function compares the user's guess with the secret word and provides feedback.

```python
def check_guess(guess_word, secret_word):
    global attempts
    attempts += 1
    feedback = []
    for i in range(len(guess_word)):
        if guess_word[i] == secret_word[i]:
            feedback.append("Correct!")
        elif guess_word[i] in secret_word:
            feedback.append("Wrong Position!")
        else:
            feedback.append("Incorrect!")
    return feedback
```

**Algorithm:**
1. The function increments the `attempts` counter.
2. It iterates through each letter of the `guess_word`.
3. For each letter, it compares it to the corresponding letter in the `secret_word`.
4. Based on the comparison, it appends "Correct!", "Wrong Position!", or "Incorrect!" to the `feedback` list.
5. The `feedback` list is returned.

## 9. Application Execution

The application is started if the script is run directly:

```python
if __name__ == "__main__":
    app.run()
```
