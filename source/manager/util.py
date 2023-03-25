from source.util import *
import traceback

def search_path(filename) -> str:
    filename+=".jpg"
    folder_path = os.path.join(ASSETS_PATH)
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    logger.error(f"SearchPathError:{filename}")
    return None