import json
from pydantic_settings import BaseSettings, SettingsConfigDict, SettingsError

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int] | str  # может прийти как строка
    SUPPORT_ID: int
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
            
        # Преобразуем SUPPORT_ID в int если пришел как строка
        if isinstance(self.SUPPORT_ID, str):
            self.SUPPORT_ID = int(self.SUPPORT_ID)

settings = Settings()

"""
    Объяснение:

Использую pydantic-settings — безопасный способ валидировать данные из .env.

Каждый параметр типизирован, что предотвращает ошибки (ADMIN_ID — list[int]).

Можно менять окружения (dev/prod) просто через .env.

Экземпляр settings импортируется по всему проекту.
"""