from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """
    Development-specific configuration.
    """ 
    DEBUG = True
    SQLALCHEMY_ECHO = True
    MAIL_DEBUG = True