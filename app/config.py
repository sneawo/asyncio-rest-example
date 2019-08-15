import os
import re

MONGODB_HOST = 'localhost'
IN_DOCKER = bool(os.environ.get('IN_DOCKER', False))
if IN_DOCKER:
    MONGODB_HOST = 'mongo'


def clean_mongodb_uri(mongodb_uri):
    """Remove username:password."""
    return re.sub(r'//.+@', '//', mongodb_uri)


class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI', f'mongodb://{MONGODB_HOST}:27017/items')
    PORT = int(os.environ.get('PORT', 8080))
    DEBUG = bool(os.environ.get('DEBUG', False))

    def __str__(self) -> str:
        return f'mongodb_uri={clean_mongodb_uri(self.MONGODB_URI)}, debug={self.DEBUG}'


class TestConfig(Config):
    MONGODB_URI = os.environ.get('MONGODB_TEST_URI', f'mongodb://{MONGODB_HOST}:27017/items_test')
    DEBUG = True
