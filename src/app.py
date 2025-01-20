"""
This module initializes and runs a Flask application.

It imports and configures:
- The Flask application (`app`) with settings from `Config`.
- The database (`db`) and initializes it with the application.
- The routes blueprint (`routes`) for handling application routes.

The application creates all database tables when the app context is active.
Finally, it starts the Flask development server if the script is run directly.
"""

from flask import Flask

from db import db
from db.config import Config
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
