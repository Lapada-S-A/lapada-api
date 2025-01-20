"""
This module defines the database configuration for the application.

It uses environment variables loaded from a `.env` file to configure
the SQLAlchemy database connection.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for SQLAlchemy database settings.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The database connection URI.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable modification tracking.
    """

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
