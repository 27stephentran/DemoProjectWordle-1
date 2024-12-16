from flask import Flask, request, render_template
from random import choice
import database
import os

leaderboard = []
attempts = 1
secret_word = ""
name = ''
if not os.path.exists("wordle.db"):
    database.make_database()
WORDS = database.get_words()
print(WORDS)

def choose_word():
    global WORDS
    chosen_word = choice(WORDS) 
    word_id = chosen_word[0]
    secret_word = chosen_word[1].upper()
    return word_id, secret_word

word_id, secret_word = choose_word()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wordle_page", methods=["GET", "POST"])
def wordle_page():
    global word_id, secret_word, leaderboard, attempts, name
    print(secret_word)
    guess = [""] * len(secret_word)
    if request.method == "POST":
        name = request.form.get("name_input").upper()
        guess = [request.form.get(f"letter{i+1}", "").upper()
                 for i in range(len(secret_word))]
        guess_word = "".join(guess)

        if len(guess_word) != len(secret_word):
            return render_template("wordle_page.html", error="Not Enough Letters", word_length=len(secret_word), guess=guess, leaderboard = leaderboard, name = name)
        
        feedback = check_guess(guess_word, secret_word)

        if guess_word == secret_word:
            database.add_player(name, attempts, word_id)
            leaderboard = database.get_leaderboard(word_id)
            return render_template("wordle_page.html", success=True, feedback=feedback, word_length=len(secret_word), guess=guess, leaderboard = leaderboard, name = name)
        
        return render_template("wordle_page.html", feedback=feedback, word_length=len(secret_word), guess=guess, leaderboard = leaderboard, name = name)
    return render_template("wordle_page.html", word_length=len(secret_word), guess=guess, leaderboard = leaderboard, name = name)

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

if __name__ == "__main__":
    app.run()
