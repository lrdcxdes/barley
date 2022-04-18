from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buy_case_kb = InlineKeyboardMarkup(row_width=1)
buy_case_kb.add(InlineKeyboardButton(text='🛒 Купить кейс', switch_inline_query_current_chat='Кейс купить '))

open_case_kb = InlineKeyboardMarkup(row_width=1)
open_case_kb.add(InlineKeyboardButton(text='📦 Открыть кейс', switch_inline_query_current_chat='Кейс открыть '))

play_casino_kb = InlineKeyboardMarkup(row_width=1)
play_casino_kb.add(InlineKeyboardButton(text='🎰 Играть ещё', switch_inline_query_current_chat='Казино '))

play_dice_kb = InlineKeyboardMarkup(row_width=1)
play_dice_kb.add(InlineKeyboardButton(text='🎲 Играть ещё', switch_inline_query_current_chat='Кубик '))

play_nvuti_kb = InlineKeyboardMarkup(row_width=1)
play_nvuti_kb.add(InlineKeyboardButton(text='📉 Играть ещё', switch_inline_query_current_chat='Нвути '))

play_flip_kb = InlineKeyboardMarkup(row_width=1)
play_flip_kb.add(InlineKeyboardButton(text='🪙 Играть ещё', switch_inline_query_current_chat='Флип '))

play_roulette_kb = InlineKeyboardMarkup(row_width=1)
play_roulette_kb.add(InlineKeyboardButton(text='🔴 Играть ещё', switch_inline_query_current_chat='Рулетка '))

play_bowling_kb = InlineKeyboardMarkup(row_width=1)
play_bowling_kb.add(InlineKeyboardButton(text='🎳 Играть ещё', switch_inline_query_current_chat='Боулинг '))

play_darts_kb = InlineKeyboardMarkup(row_width=1)
play_darts_kb.add(InlineKeyboardButton(text='🎯 Играть ещё', switch_inline_query_current_chat='Дартс '))

play_cnb_kb = InlineKeyboardMarkup(row_width=1)
play_cnb_kb.add(InlineKeyboardButton(text='🧻 Играть ещё', switch_inline_query_current_chat='КНБ '))
