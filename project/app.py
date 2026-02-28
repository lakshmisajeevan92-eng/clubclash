from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length, use_upper, use_digits, use_symbols):
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))

def password_strength(password):
    score = 0
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if len(password) >= 12: score += 1

    levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    return levels[min(score, 4)]

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    strength = ""

    if request.method == "POST":
        length = int(request.form["length"])
        use_upper = "upper" in request.form
        use_digits = "digits" in request.form
        use_symbols = "symbols" in request.form

        password = generate_password(length, use_upper, use_digits, use_symbols)
        strength = password_strength(password)

    return render_template("index.html", password=password, strength=strength)

if __name__ == "__main__":
    app.run(debug=True)