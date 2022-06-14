# ===== Конфиг лог для логгера =====#
import logging
from configs.config import LOG_PATH

# Формат записи логов
_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"


# Обработчик логов для записи в файл
def get_file_handler():
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


# Обработчик логов для вывода в консоль
def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


# Метод для вызова логгера
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
