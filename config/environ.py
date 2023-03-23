import os
from dotenv import load_dotenv

load_dotenv()


class Environ:

    # 장고 시크릿 키
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # rootDB
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PORT = os.environ.get('DB_PORT')
    DB_ENGINE = os.environ.get('DB_ENGINE')

    # 구글 메일 설정
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

