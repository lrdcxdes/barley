from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


help_kb = InlineKeyboardMarkup(row_width=2)
help_kb.insert(InlineKeyboardButton(text='Ⓜ️ Основное', callback_data='help_main'))
help_kb.insert(InlineKeyboardButton(text='Игры 🎮', callback_data='help_games'))
help_kb.insert(InlineKeyboardButton(text='👩🏿‍🏭 Работы', callback_data='help_work'))
help_kb.insert(InlineKeyboardButton(text='Имущество 🚙', callback_data='help_imush'))
help_kb.insert(InlineKeyboardButton(text='💫 Уникальное', callback_data='help_unik'))
help_kb.insert(InlineKeyboardButton(text='Прочее 🪠', callback_data='help_other'))

back_kb = InlineKeyboardMarkup(row_width=1)
back_kb.add(InlineKeyboardButton(text='🔙 Назад', callback_data='help_back'))
