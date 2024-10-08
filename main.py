from flask import Flask, request, render_template
import random

WORDS = ["apple", "grade", "grape", "melon"]

secret_word = random.choice(WORDS).upper()
app = Flask(__name__)

@app.route("/", method = ["GET", "POST"])
def index():
    guess = [''] * len(secret_word)
    if request.method == "POST":
        guess = [
            request.form.get(f'letter{i+1}', '').upper()
            for i in range(len(secret_word))
        ]

        guess_word = "".join(guess)

        if len(guess_word) != len(secret_word):
            return render_template("index.html", error = "Word must be the correct length", word_length = len(secret_word), guess= guess)
        feedback = check_guess(guess_word, secret_word)

        if guess_word == secret_word:
            return render_template("index.html", feedback=feedback, success=True, word_length = len(secret_word), guess = guess)
        
        return render_template("index.html", feedback=feedback, guess = guess, word_length = len(secret_word))
    return render_template("index.html", word_length = len(secret_word), guess = guess)

def check_guess(guess, secret_word):
    feedback = []
    for i in range(len(secret_word)):
        if guess_word[i] == secret_word[i]:
            feedback.append("Match")
        elif guess_word[i] in secret_word:
            feedback.append("Wrong position")
        else:
            feedback.append("Wrong")

    return feedback

if __name__ == "__main__":
    app.run(debug = True)
        