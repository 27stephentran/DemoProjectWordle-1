from flask import Flask, request, render_template
from random import choice




WORDS = ["apple", "maple", "Pneumonoultramicroscopicsilicovolcanoconiosis", "hello"]

# secret_word = choice(WORDS).upper()\

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/wordle_page", methods = ["GET", "POST"])
def wordle_page():
    guess = [""] * len(secret_word)
    if request.method == "POST":
        guess = [request.form.get(f"letter{i+1}", "").upper()
                 for i in range(len(secret_word))]
        guess_word = "".join(guess)

        if len(guess_word) != len(secret_word):
            return render_template("wordle_page.html", error = "Not Enough Word", word_length = len(secret_word), guess = guess)
        feedback = check_guess(guess_word, secret_word)
        if guess_word == secret_word:
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