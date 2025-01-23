#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)


class Config:
    """Configuration for Flask-Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


# Instantiate Babel
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve a user dictionary based on login_as parameter."""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Executed before each request to
    find and set the user in the global object."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    # Check if 'locale' parameter exists in the URL query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user["locale"]
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index page."""
    if g.user:
        username = g.user["name"]
        welcome_message = _("logged_in_as", username=username)
    else:
        welcome_message = _("not_logged_in")
    return render_template('5-index.html', welcome_message=welcome_message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
