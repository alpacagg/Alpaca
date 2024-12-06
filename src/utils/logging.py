import logging
import sys
from typing import Optional, List, Union
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(
            self,
            name: str = 'AppLogger',
            level: int = logging.INFO,
            log_dir: Optional[str] = 'logs',
            max_file_size_mb: int = 10,
            backup_count: int = 3
    ):
        """
        Initialize a configurable, advanced logger.

        Args:
            name (str): Logger name
            level (int): Logging level
            log_dir (str): Directory for log files
            max_file_size_mb (int): Max log file size in MB
            backup_count (int): Number of backup log files to keep
        """
        self.name = name
        self.level = level
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.handlers.clear()

        # Ensure log directory exists
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)

        # Formatter
        self._formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler(max_file_size_mb, backup_count)

    def _setup_console_handler(self):
        """Configure console logging handler."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._formatter)
        self._logger.addHandler(console_handler)

    def _setup_file_handler(self, max_file_size_mb: int, backup_count: int):
        """Configure rotating file logging handler."""
        log_file = self._log_dir / f'{self.name}.log'
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size_mb * 1024 * 1024,
            backupCount=backup_count
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._formatter)
        self._logger.addHandler(file_handler)

    def log(self, message: str, level: int = logging.INFO):
        """
        Log a message at specified level.

        Args:
            message (str): Log message
            level (int): Logging level
        """
        if level == logging.DEBUG:
            self._logger.debug(message)
        elif level == logging.INFO:
            self._logger.info(message)
        elif level == logging.WARNING:
            self._logger.warning(message)
        elif level == logging.ERROR:
            self._logger.error(message)
        elif level == logging.CRITICAL:
            self._logger.critical(message)

    def debug(self, message: str):
        """Log debug message."""
        self._logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self._logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self._logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """
        Log error message.

        Args:
            message (str): Error message
            exc_info (bool): Include exception traceback
        """
        self._logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """
        Log critical message.

        Args:
            message (str): Critical message
            exc_info (bool): Include exception traceback
        """
        self._logger.critical(message, exc_info=exc_info)

    def set_level(self, level: Union[int, str]):
        """
        Set logging level dynamically.

        Args:
            level (Union[int, str]): Logging level
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)
