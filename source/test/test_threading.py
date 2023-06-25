import threading, time
from loguru import logger

class CustomException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.stop_manager_flag = True

def excepthook(args):
    print(args.exc_value)
    logger.exception(args.exc_value)

threading.excepthook = excepthook

def func1():
    for i in range(10):
        print(i)
        time.sleep(0.2)
        if i==3:
            raise CustomException

        
t1 = threading.Thread(target=func1)
t1.start()

while 1:
    time.sleep(1)
    print('...')