'''
logger utility
'''
import logging


class Logger(logging.getLoggerClass()):
    """
    # Inheritance
    """
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def critical(self, msg, *args, **kwargs):
        self.handlers = self.root.handlers
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.handlers = self.root.handlers
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.handlers = self.root.handlers
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.handlers = self.root.handlers
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.handlers = self.root.handlers
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def setup_log(self, log_file=None, console_level=logging.DEBUG):
        formatter = logging.Formatter(fmt='%(asctime)-15s | %(name)-15s:%(lineno)-4s | %(levelname)-7s | %(message)-10s',
                                      datefmt='%Y-%m-%d %H:%M:%S', )
        self.setLevel(logging.DEBUG)
        root_logger = self.root

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(console_level)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)

        if log_file is not None:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            root_logger.addHandler(file_handler)
