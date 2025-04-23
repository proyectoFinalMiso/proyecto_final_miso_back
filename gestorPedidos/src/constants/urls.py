from os import getenv


# External routes
def database_host():
    DB_HOST = getenv('DB_HOST')
    DB_USER = getenv('DB_USER')
    DB_PWD = getenv('DB_PWD')
    DB_NAME = getenv('DB_NAME')

    DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'
    return DATABASE_URI


PRODUCT_URL = getenv('MS_PRODUCTOS_URL')
STORE_URL = getenv('MS_BODEGA_URL')
