from dotenv import dotenv_values


config = dotenv_values(".env")

API_KEY = config['API_KEY']
SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
