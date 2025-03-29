from os import getenv

# External routes
def database_host():
    DB_HOST = getenv('DB_HOST', 'localhost')
    DB_USER = getenv('DB_USER', 'postgres')
    DB_PWD = getenv('DB_PWD', 'postgres')
    DB_NAME = getenv('DB_NAME', 'postgres')

    DATABASE_URI = f'postgresql+pg8000://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'
    return DATABASE_URI 
