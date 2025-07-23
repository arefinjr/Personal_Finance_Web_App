import tempfile
from .base import BaseConfig

class TestingConfig(BaseConfig):
    """
    Testing-specific configuration.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    MAIL_SUPPRESS_SEND = True
