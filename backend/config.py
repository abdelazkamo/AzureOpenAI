import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    SECRET_KEY = "SECTECTCHATAPI"
    UPLOAD_FOLDER = "./uploads"
    SPARSE_STORAGE = "./sparse_storage"
    MAX_CONTENT_LENGTH = 20000 * 1024 * 1024
    BODY_TIMEOUT = 60 * 20
    RESPONSE_TIMEOUT = 60 * 20

    # AZURE_GPT
    AZURE_GPT_API_BASE = os.getenv("AZURE_GPT_API_BASE")
    AZURE_GPT_API_KEY = os.getenv("AZURE_GPT_API_KEY")
    AZURE_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")
    AZURE_GPT_API_VERSION = os.getenv("AZURE_GPT_API_VERSION")
    # DB CREDENTIALS
    DRIVER = os.getenv("DRIVER")
    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DATABASE")
    UID = os.getenv("UID")
    PWD = os.getenv("PWD")
