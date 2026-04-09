import logging
import os
import sys

class LoggerManager:
    """Gerencia uma instância simples de logger (singleton)."""
    _logger = None


    @classmethod
    def get_logger(cls, name=None):
        """Retorna um logger configurado para arquivo e console."""
        if cls._logger is not None:
            return cls._logger

        if name is None:
            name = __name__

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        log_dir = './logs'
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(os.path.join(log_dir, 'logs.log'), mode='a')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        utf8_stream = open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
        console_handler = logging.StreamHandler(utf8_stream)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._logger = logger
        return logger

    @staticmethod
    def log_key_value(key, value, filename, logger=None):
        """Helper opcional para logar pares chave/valor."""
        if logger is None:
            logger = LoggerManager.get_logger()
        logger.info(f"{filename}: {key} = {value}")
