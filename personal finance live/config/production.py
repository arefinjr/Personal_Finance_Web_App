import os
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """
    Production-specific configuration.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    MAIL_DEBUG = False