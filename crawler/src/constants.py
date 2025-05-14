import os
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.environ.get("DATA_PATH")
THREAD_COUNT = 10
