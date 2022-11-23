import logging

from source.webio import manager


class WebioHandler(logging.NullHandler):

    def handle(self, record: logging.LogRecord) -> None:
        manager.get_page('Main').logout(logging.Formatter.formatMessage(record))

