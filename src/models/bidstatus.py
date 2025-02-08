"""
Module for representing status in the database.
"""
from enum import Enum


class BidStatus(Enum):
    """
    Represents the possible statuses.
    """

    ACTIVE = '1'
    EXPIRED = '2'
    WINNER = '3'
