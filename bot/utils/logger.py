import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

"""Объяснение:

Централизованный логгер для всех модулей.

Используется в main.py и других местах.

Можно потом заменить на loguru или систему логов с сохранением в файл."""