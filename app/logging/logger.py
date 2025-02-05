import logging
from logging import handlers

class Logger(object):

    def __init__(self, filename):
        self.log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        logging.getLogger("uvicorn").propagate = False
        logging.basicConfig(filename=filename, format=self.log_format, datefmt=self.date_format, level=logging.INFO)

    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

logger = Logger('app/logs/app_logs.log')
logging.getLogger("multipart").setLevel(logging.ERROR)

