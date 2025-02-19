import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger
import sys


load_dotenv(find_dotenv())

logger.remove(0)
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss zz}</green> <cyan>{function}</cyan> <level>{message}</level>",
    level="INFO",
)


PROJECT_NAME = os.getenv("PROJECT_NAME", "Computer Vision Model Training API")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
