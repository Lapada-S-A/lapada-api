"""
This module initializes the SQLAlchemy database instance.

The `db` object is used to interact with the application's database
and should be imported wherever database operations are required.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
