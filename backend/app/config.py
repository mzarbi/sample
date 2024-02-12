class Config:
    """Base config."""
    SECRET_KEY = 'your_secret_key'
    SWAGGER = {
        'title': 'My API',
        'uiversion': 3
    }


class DevelopmentConfig(Config):
    DEBUG = True
    # Database setup, etc.


class ProductionConfig(Config):
    DEBUG = False
    # Production configs
