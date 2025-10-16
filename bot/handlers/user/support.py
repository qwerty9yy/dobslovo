# from aiogram import Router, F
# from aiogram.types import Message, CallbackQuery
# from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
# from bot.filters.support import IsSupport
# from bot.handlers.user.menu_command import show_start_menu
# from bot.keyboards.user.support import get_menu_support
# from bot.utils.states import SupportState

# # Создаем роутеры
# support_router = Router() # Для пользователей
# support_admin_router = Router() # Для поддержки
# support_admin_router.message.filter(IsSupport()) # Фильтр для поддержки

# @support_router.message(Command('support'))
# @support_router.callback_query(F.data == 'support')
# async def show_menu_support(message_or_call, state: FSMContext):
#     """Меню поддержки"""
#     text = (
#         "💬 Напишите нам\n\n"
#         "Опишите ваш вопрос, проблему или пожелание — и мы обязательно вам ответим!\n\n"
#         "Также вы можете:\n"
#         "• 🛍️ Заказать продукцию редакции\n"
#         "• 📚 Узнать о новых проектах\n"
#         "• 💡 Предложить сотрудничество\n\n"
#         "Мы на связи и поможем решить любой вопрос!"
#     )
#     markup = get_menu_support()
#     if isinstance(message_or_call, CallbackQuery):
#         # Для колбэков всегда редактируем сообщение
#         await message_or_call.message.edit_text(text, reply_markup=markup)
#     else:
#         # Для сообщений всегда отправляем новое
#         await message_or_call.answer(text, reply_markup=markup)
#     await state.set_state(SupportState.waiting_for_question)

# # Отмена вопроса
# @support_router.callback_query(F.data == 'cancel_support')
# async def cancel_support(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.answer('❌ Вопрос отменен', show_alert=False)
#     await show_start_menu(callback, edit=True)

# # Обработка вопроса от пользователя
# @support_router.message(StateFilter(SupportState.waiting_for_question))
# async def process_user_question(message: Message, state: FSMContext):
#     """Обработка вопроса от пользователя"""
    