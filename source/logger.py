from loguru import logger
import types
warned_dict={}
def warning_once(self, message):
    is_warned = warned_dict.setdefault(message, False)
    if not is_warned:
        self.warning(message)
        warned_dict[message]=True

logger.warning_once = types.MethodType(warning_once, logger)

if __name__ == "__main__":
    logger.warning_once("123")
    logger.warning_once("123")
    logger.warning_once("123")