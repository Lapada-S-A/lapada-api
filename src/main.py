import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import routes
from db.config import Config
from db import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
