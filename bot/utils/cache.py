# # универсальный декоратор кеша
# import json
# import os
# import time
# from functools import wraps
# from typing import Callable, Any

# def cache_json(ttl: int = 86400):
#     """
#     Асинхронный декоратор для кеширования результата функции в JSON-файл.
#     ttl — время жизни кеша (в секундах), по умолчанию 24 часа.
#     """

#     def decorator(func: Callable):
#         cache_file = f"/tmp/{func.__name__}.json"

#         @wraps(func)
#         async def wrapper(*args, **kwargs) -> Any:
#             # 1️⃣ Проверяем, есть ли актуальный кеш
#             if os.path.exists(cache_file):
#                 mtime = os.path.getmtime(cache_file)
#                 if (time.time() - mtime) < ttl:
#                     try:
#                         with open(cache_file, "r", encoding="utf-8") as f:
#                             return json.load(f)
#                     except Exception as e:
#                         print(f"⚠️ Ошибка чтения кеша {cache_file}: {e}")

#             # 2️⃣ Если кеш устарел — вызываем функцию
#             try:
#                 result = await func(*args, **kwargs)
#             except Exception as e:
#                 print(f"⚠️ Ошибка при выполнении {func.__name__}: {e}")
#                 return None

#             # 3️⃣ Сохраняем результат в файл
#             try:
#                 with open(cache_file, "w", encoding="utf-8") as f:
#                     json.dump(result, f, ensure_ascii=False, indent=2)
#             except Exception as e:
#                 print(f"⚠️ Ошибка записи кеша {cache_file}: {e}")

#             return result

#         return wrapper

#     return decorator