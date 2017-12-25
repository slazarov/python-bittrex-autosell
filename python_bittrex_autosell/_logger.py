import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__package__).addHandler(NullHandler())


def add_stream_logger(level=logging.DEBUG, file_name=False):
    logger = logging.getLogger(__package__)
    logger.setLevel(level)
    if file_name is not False:
        logger.addHandler(_get_file_handler(file_name))
    logger.addHandler(_get_stream_handler())
    if __name__ != '__main__':
        return logger


def add_file_handler(logger_name, file_name=None):
    logs = logging.getLogger(logger_name)
    logs.addHandler(_get_file_handler(file_name))
    return logs


def remove_stream_logger():
    logger = logging.getLogger(__package__)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    logger.addHandler(NullHandler())


def _get_stream_handler(level=logging.DEBUG):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(_get_formatter())
    return handler


def _get_file_handler(file_name):
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(_get_formatter())
    return file_handler


def _get_formatter():
    msg_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(msg_format, date_format)
    return formatter
