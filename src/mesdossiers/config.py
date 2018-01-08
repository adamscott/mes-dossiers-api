import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=os.getenv('POSTGRES_USER', 'postgres'),
        pw=os.getenv('POSTGRES_PASSWORD', ''),
        url=os.getenv('POSTGRES_URL', 'localhost:5432'),
        db=os.getenv('POSTGRES_DB', 'mes-dossiers')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
