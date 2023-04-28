from source.logger import logger
import traceback

LEVEL_WARN = "WARN"
LEVEL_ERR = "ERR"
LEVEL_CRI = "CRITICAL"

def get_name(x):
    (filename, line_number, function_name, text) = x
    # = traceback.extract_stack()[-2]
    return text[:text.find('=')].strip()
class ERR_CODE():
    def __init__(self, level="WARN", message=None, err_id:int=None, addition_id:int=None) -> None:
        self.level = level
        if message == None:
            message = get_name(traceback.extract_stack()[-2])
        self.message = message
        self.err_id = err_id
        if addition_id != None:
            self.addition_id = f"_{addition_id}"
        self.str = f"{self.message}_{self.err_id}{self.addition_id}"

    def __str__(self):
        return self.str

    def log(self):
        if self.level=='WARN':
            logger.warning(self.str)
        elif self.level=='ERR':
            logger.warning(self.str)
        elif self.level=='CRITICAL':
            logger.warning(self.str)
    