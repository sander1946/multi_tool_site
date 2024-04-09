import os
import time
from src.config import config
def remove_expired_files(path) -> None:
    filenames = next(os.walk(path), (None, None, []))[2]  # [] if no file
    for file in filenames:
        file_path = os.path.join(path, file)
        if os.path.getmtime(file_path) < time.time() - config.EXPIRE_TIME: 
            os.remove(file_path)
            print(f"File {file} removed due to expiration.")