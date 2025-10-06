import json
from pydantic_settings import BaseSettings, SettingsConfigDict, SettingsError

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int] | str  # может прийти как строка
    DATABASE_URL: str = "sqlite+aiosqlite:///bot.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def model_post_init(self, __context):
        """Преобразуем ADMIN_IDS, если пришли в виде строки JSON."""
        if isinstance(self.ADMIN_IDS, str):
            try:
                # пытаемся распарсить как JSON-список
                self.ADMIN_IDS = json.loads(self.ADMIN_IDS)
            except json.JSONDecodeError:
                # fallback: CSV формат через запятую
                self.ADMIN_IDS = [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]
            except Exception as e:
                raise SettingsError(f"Ошибка в формате ADMIN_IDS: {e}")

settings = Settings()

"""
    Объяснение:

Использую pydantic-settings — безопасный способ валидировать данные из .env.

Каждый параметр типизирован, что предотвращает ошибки (ADMIN_ID — int).

Можно менять окружения (dev/prod) просто через .env.

Экземпляр settings импортируется по всему проекту.
"""