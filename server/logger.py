import sys
import logging
import os

APP_NAME = os.environ.get('APP_NAME','no app name')
LOG_LEVEL = os.environ.get('LOG_LEVEL',logging.DEBUG)
logger = logging.getLogger(APP_NAME)
logger.setLevel(LOG_LEVEL)
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(LOG_LEVEL)
file_handler = logging.FileHandler('./logs/last_run.log',mode='w')
file_handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter("%(asctime)s\t[%(levelname)s]\t%(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# logging.basicConfig(stream=sys.stderr,\
#     level=logging.getLevelName(level=LOG_LEVEL),\
#     format="%(asctime)s\t[%(levelname)s]\t%(message)s")

# logger = logging.Logger(name=APP_NAME)

###
# LOGGING FACTORY
#
# def make_logger(is_development=False):
#     """
#     Sets up logging with a standard format, creates a logger instance and returns it.
#     :param Bool is_development: controls whether to mark the logger's level as DEBUG or
#            as specified in the config file
#     :rtype: logging.Logger.
#     :return: logger instance.
#     """
#     _logger = logging.Logger(name=APP_NAME)

#     if is_development:
#         _logger.setLevel(logging.DEBUG)

#     handler = logging.StreamHandler()
#     _logger.addHandler(handler)
#     return _logger


# def get_logger():
    # """
    # Returns the application's logger instance by name.
    # :rtype: logging.Logger.
    # :return: logger instance.
    # """
    # _logger = logging.getLogger(APP_NAME)

    # if isinstance(_logger, logging.RootLogger):
    #     _logger = make_logger()

    # return _logger