"""
Module for representing status in the database.
"""
from enum import Enum


class Status(Enum):
    """
    Represents the possible statuses.

    Attributes:
        PENDING: The status is pending.
        ACTIVE: The status is active.
        FINISHED: The status is finished.
        REJECTED: The status is rejected.
        CANCELED: The status is canceled.
    """

    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    FINISHED = 'FINISHED'
    REJECTED = 'REJECTED'
    CANCELED = 'CANCELED'
