from pathlib import Path
from dotenv import load_dotenv
import os

#load environment variables from .env file
load_dotenv()

#project Paths

#root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

#Data folders
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"
POPPLER_PATH = os.getenv("POPPLER_PATH")
#OCR Configuration

OCR_LANGUAGE = "fr"

USE_GPU = False

#Supported File Types

SUPPORTED_EXTENSIONS = [
    ".pdf"
]
#Future Database Configuration

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")