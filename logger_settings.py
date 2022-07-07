import logging.handlers


class CustomFormatter(logging.Formatter):
    """Logging colored formatter,
    adapted from https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/"""

    green = '\033[0;32m\033[3m'
    grey = '\x1b[38;21m\033[3m'
    blue = '\x1b[38;5;39m\033[3m'
    yellow = '\x1b[38;5;226m\033[3m'
    red = '\x1b[38;5;196m\033[3m'
    bold_red = '\x1b[31;1m\033[3m'
    reset = '\x1b[0m'

    def __init__(self, fmt: str, datefmt: str, style: str):
        super().__init__()
        self.datefmt = datefmt
        self.style = style
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.green + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt
        }

    def format(self, record: logging.LogRecord) -> str:
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format, self.datefmt, self.style)  # type: ignore
        return formatter.format(record)
