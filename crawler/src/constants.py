import os

try:
    DATA_PATH = os.environ["DATA_PATH"]
except KeyError:
    DATA_PATH = "./data"

THREAD_COUNT = 10
