import logging
from source.webio import manager


class WebioHandler(logging.NullHandler):

    def handle(self, record: logging.LogRecord) -> None:
        manager.get_page('Main').logout(logging.Formatter.formatMessage(record))

def webio_poster(x):
    manager.get_page('Main').logout(x)

# webio_handler = WebioHandler()