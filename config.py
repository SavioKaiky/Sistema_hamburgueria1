import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "9076e998f5f666109628be0b24b58264ed365d87a2e57ea018894dec498f6a5b"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@localhost/Sistema_Hamburgueria"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False