#!/usr/bin/env python3
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)

class Config:
    """Configuration for Flask-Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

# Instantiate Babel
babel = Babel(app)

@app.route('/')
def index():
    """Render the index page."""
    return render_template('1-index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
