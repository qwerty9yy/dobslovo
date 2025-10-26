from loguru import logger
import sys

# Настройка формата логов
logger.remove()  # Удаляем стандартный обработчик
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}", level="INFO")

# Логи в файл (самый простой способ)
logger.add(
    "bot/logs/bot.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",  # Ротация при достижении 10 МБ
    retention="30 days",  # Хранить логи 30 дней
    compression="zip"  # Сжимать старые логи
)

__all_ = ["logger"] # Экспортируем логгер для использования в других модулях

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
# )

# logger = logging.getLogger(__name__)

"""Объяснение:

Централизованный логгер для всех модулей.

Используется в main.py и других местах.

Можно потом заменить на loguru или систему логов с сохранением в файл."""