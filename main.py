from flask import Flask, request, render_template
from random import choice
import database
import os

if not os.path.exists("wordle.db"):
    database.main_database()
    database.add_words()
    
WORDS = database.get_words()
print(WORDS)




def choose_word():
    global WORDS
    choosen_word = choice(WORDS)
    word_id = choosen_word[0]
    secret_word = choosen_word[1]
    return word_id, secret_word



app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

word_id = None
@app.route("/wordle_page", methods = ["GET", "POST"])
def wordle_page():
    global word_id
    attempts = 0
    if not word_id:
        word_id, secret_word = choose_word()
    print(secret_word)
    guess = [""] * len(secret_word)
    if request.method == "POST":
        name = request.form.get("name_input").upper()
        guess = [request.form.get(f"letter{i+1}", "").upper()
                 for i in range(len(secret_word))]
        guess_word = "".join(guess)
        if request.form.get("submit"):
            attempts += 1
        if len(guess_word) != len(secret_word):
            return render_template("wordle_page.html", error = "Not Enough Word", word_length = len(secret_word), guess = guess)
        feedback = check_guess(guess_word, secret_word)
        if guess_word == secret_word:
            database.add_player(name, attempts, word_id)
            word_id = None
            return render_template("wordle_page.html", success = True, feedback = feedback, word_length = len(secret_word), guess = guess)
        
        return render_template("wordle_page.html", feedback = feedback, word_length = len(secret_word), guess = guess)
    return render_template("wordle_page.html",word_length = len(secret_word), guess = guess)

def check_guess(guess_word, secret_word):
    feedback = []
    for i in range(len(guess_word)):
        if guess_word[i] == secret_word[i]:
            feedback.append("Correct!")
        elif guess_word[i] in secret_word:
            feedback.append("Wrong Position!")
        else:
            feedback.append("Incorrect!")
    return feedback
if __name__ == "__main__":
    app.run()