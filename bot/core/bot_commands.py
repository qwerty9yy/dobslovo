from aiogram.types import BotCommand

def get_bot_commands() -> list[BotCommand]:
    """Возвращает список команд бота."""
    return [
        BotCommand(command='/start', description='Главное меню'),
        BotCommand(command='/contacts', description='Контакты'),
        BotCommand(command='/about', description='О нас'),
        BotCommand(command='/donate', description='Поддержать редакцию'),
        BotCommand(command='/products', description='Продукция'),
        BotCommand(command='/newspaper', description='Газета')
    ]