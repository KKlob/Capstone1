from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    """Show homepage all users land on"""

    return render_template('main.html')