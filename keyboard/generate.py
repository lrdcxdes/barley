from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buy_ferm_kb = InlineKeyboardMarkup(row_width=1)
buy_ferm_kb.add(InlineKeyboardButton(text='🛒 Купить ферму', switch_inline_query_current_chat='Ферма купить '))

bitcoin_kb = InlineKeyboardMarkup(row_width=2)
bitcoin_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Ферма снять'))
bitcoin_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Ферма продать'))
bitcoin_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Ферма оплатить'))
bitcoin_kb.insert(InlineKeyboardButton(text='Купить видеокарты 📼', switch_inline_query_current_chat='Видеокарты купить 1'))

show_balance_kb = InlineKeyboardMarkup(row_width=1)
show_balance_kb.add(InlineKeyboardButton(text='💰 Баланс', switch_inline_query_current_chat='Баланс'))

show_ferm_kb = InlineKeyboardMarkup(row_width=1)
show_ferm_kb.add(InlineKeyboardButton(text='🖥️ Моя ферма', switch_inline_query_current_chat='Ферма'))

buy_business_kb = InlineKeyboardMarkup(row_width=1)
buy_business_kb.add(InlineKeyboardButton(text='🛒 Купить биз', switch_inline_query_current_chat='Биз купить '))

show_business_kb = InlineKeyboardMarkup(row_width=1)
show_business_kb.add(InlineKeyboardButton(text='🧑🏿‍💼 Мой бизнес', switch_inline_query_current_chat='Биз'))

business_kb = InlineKeyboardMarkup(row_width=2)
business_kb.insert(InlineKeyboardButton(text='Снять 💸', switch_inline_query_current_chat='Биз снять'))
business_kb.insert(InlineKeyboardButton(text='Налог 💲', switch_inline_query_current_chat='Биз налог'))
business_kb.insert(InlineKeyboardButton(text='Продать 💰', switch_inline_query_current_chat='Биз продать'))
business_kb.insert(InlineKeyboardButton(text='Открыть 🟢', switch_inline_query_current_chat='Биз открыть'))

show_inv_kb = InlineKeyboardMarkup(row_width=1)
show_inv_kb.add(InlineKeyboardButton(text='🎒 Мой инвентарь', switch_inline_query_current_chat='Инв'))

buy_airplane_kb = InlineKeyboardMarkup(row_width=1)
buy_airplane_kb.add(InlineKeyboardButton(text='🛒 Купить самолёт', switch_inline_query_current_chat='Самолёт купить'))

airplane_kb = InlineKeyboardMarkup(row_width=2)
airplane_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Самолёт снять'))
airplane_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Самолёт продать'))
airplane_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Самолёт оплатить'))
airplane_kb.insert(InlineKeyboardButton(text='Лететь ✈️', switch_inline_query_current_chat='Самолёт лететь'))

show_airplane_kb = InlineKeyboardMarkup(row_width=1)
show_airplane_kb.add(InlineKeyboardButton(text='✈️ Мой самолёт', switch_inline_query_current_chat='Самолёт'))

buy_car_kb = InlineKeyboardMarkup(row_width=1)
buy_car_kb.add(InlineKeyboardButton(text='🛒 Купить машину', switch_inline_query_current_chat='Машина купить'))

car_kb = InlineKeyboardMarkup(row_width=2)
car_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Машина снять'))
car_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Машина продать'))
car_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Машина оплатить'))
car_kb.insert(InlineKeyboardButton(text='Ехать 🛻', switch_inline_query_current_chat='Машина ехать'))

show_car_kb = InlineKeyboardMarkup(row_width=1)
show_car_kb.add(InlineKeyboardButton(text='🛻 Моя машина', switch_inline_query_current_chat='Машина'))

buy_moto_kb = InlineKeyboardMarkup(row_width=1)
buy_moto_kb.add(InlineKeyboardButton(text='🛒 Купить мото', switch_inline_query_current_chat='Мото купить'))

moto_kb = InlineKeyboardMarkup(row_width=2)
moto_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Мото снять'))
moto_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Мото продать'))
moto_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Мото оплатить'))
moto_kb.insert(InlineKeyboardButton(text='Ехать 🏍️', switch_inline_query_current_chat='Мото ехать'))

show_moto_kb = InlineKeyboardMarkup(row_width=1)
show_moto_kb.add(InlineKeyboardButton(text='🏍️ Мой мотоцикл', switch_inline_query_current_chat='Мото'))

buy_rocket_kb = InlineKeyboardMarkup(row_width=1)
buy_rocket_kb.add(InlineKeyboardButton(text='🛒 Купить ракету', switch_inline_query_current_chat='Ракета купить'))

rocket_kb = InlineKeyboardMarkup(row_width=2)
rocket_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Ракета снять'))
rocket_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Ракета продать'))
rocket_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Ракета оплатить'))
rocket_kb.insert(InlineKeyboardButton(text='Лететь 🚀', switch_inline_query_current_chat='Ракета лететь'))

show_rocket_kb = InlineKeyboardMarkup(row_width=1)
show_rocket_kb.add(InlineKeyboardButton(text='🚀 Моя ракета', switch_inline_query_current_chat='Ракета'))

buy_tank_kb = InlineKeyboardMarkup(row_width=1)
buy_tank_kb.add(InlineKeyboardButton(text='🛒 Купить танк', switch_inline_query_current_chat='Танк купить'))

tank_kb = InlineKeyboardMarkup(row_width=2)
tank_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Танк снять'))
tank_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Танк продать'))
tank_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Танк оплатить'))
tank_kb.insert(InlineKeyboardButton(text='Ехать 🪖', switch_inline_query_current_chat='Танк ехать'))

show_tank_kb = InlineKeyboardMarkup(row_width=1)
show_tank_kb.add(InlineKeyboardButton(text='🪖 Мой танк', switch_inline_query_current_chat='Танк'))

buy_vertolet_kb = InlineKeyboardMarkup(row_width=1)
buy_vertolet_kb.add(InlineKeyboardButton(text='🛒 Купить вертолёт', switch_inline_query_current_chat='Вертолёт купить'))

vertolet_kb = InlineKeyboardMarkup(row_width=2)
vertolet_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Вертолёт снять'))
vertolet_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Вертолёт продать'))
vertolet_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Вертолёт оплатить'))
vertolet_kb.insert(InlineKeyboardButton(text='Лететь 🚁', switch_inline_query_current_chat='Вертолёт лететь'))

show_vertolet_kb = InlineKeyboardMarkup(row_width=1)
show_vertolet_kb.add(InlineKeyboardButton(text='🚁 Мой вертолёт', switch_inline_query_current_chat='Вертолёт'))

buy_yaxta_kb = InlineKeyboardMarkup(row_width=1)
buy_yaxta_kb.add(InlineKeyboardButton(text='🛒 Купить яхту', switch_inline_query_current_chat='Яхта купить'))

yaxta_kb = InlineKeyboardMarkup(row_width=2)
yaxta_kb.insert(InlineKeyboardButton(text='Вывести 💸', switch_inline_query_current_chat='Яхта снять'))
yaxta_kb.insert(InlineKeyboardButton(text='Продать 🗑️', switch_inline_query_current_chat='Яхта продать'))
yaxta_kb.insert(InlineKeyboardButton(text='Налоги 💲', switch_inline_query_current_chat='Яхта оплатить'))
yaxta_kb.insert(InlineKeyboardButton(text='Ехать ⛵', switch_inline_query_current_chat='Яхта ехать'))

show_yaxta_kb = InlineKeyboardMarkup(row_width=1)
show_yaxta_kb.add(InlineKeyboardButton(text='⛵ Моя яхта', switch_inline_query_current_chat='Яхта'))

buy_house_kb = InlineKeyboardMarkup(row_width=1)
buy_house_kb.add(InlineKeyboardButton(text='🛒 Купить дом', switch_inline_query_current_chat='Дом купить '))

show_house_kb = InlineKeyboardMarkup(row_width=1)
show_house_kb.add(InlineKeyboardButton(text='🏠 Мой дом', switch_inline_query_current_chat='Дом'))

house_kb = InlineKeyboardMarkup(row_width=2)
house_kb.insert(InlineKeyboardButton(text='Снять 💸', switch_inline_query_current_chat='Дом снять'))
house_kb.insert(InlineKeyboardButton(text='Налог 💲', switch_inline_query_current_chat='Дом налог'))
house_kb.insert(InlineKeyboardButton(text='Продать 💰', switch_inline_query_current_chat='Дом продать'))
house_kb.insert(InlineKeyboardButton(text='Аренда 🟢', switch_inline_query_current_chat='Дом аренда'))

ride_car_kb = InlineKeyboardMarkup(row_width=1)
ride_car_kb.add(InlineKeyboardButton(text='🚗 Ехать ещё раз', switch_inline_query_current_chat='Машина ехать'))

ride_airplane_kb = InlineKeyboardMarkup(row_width=1)
ride_airplane_kb.add(InlineKeyboardButton(text='✈️ Лететь ещё раз', switch_inline_query_current_chat='Самолёт лететь'))

ride_moto_kb = InlineKeyboardMarkup(row_width=1)
ride_moto_kb.add(InlineKeyboardButton(text='🏍️ Ехать ещё раз', switch_inline_query_current_chat='Мото ехать'))

ride_yaxta_kb = InlineKeyboardMarkup(row_width=1)
ride_yaxta_kb.add(InlineKeyboardButton(text='⛵ Плыть ещё раз', switch_inline_query_current_chat='Яхта плыть'))

ride_rocket_kb = InlineKeyboardMarkup(row_width=1)
ride_rocket_kb.add(InlineKeyboardButton(text='🚀 Лететь ещё раз', switch_inline_query_current_chat='Ракета лететь'))

ride_tank_kb = InlineKeyboardMarkup(row_width=1)
ride_tank_kb.add(InlineKeyboardButton(text='🪖 Ехать ещё раз', switch_inline_query_current_chat='Танк ехать'))

ride_vertolet_kb = InlineKeyboardMarkup(row_width=1)
ride_vertolet_kb.add(InlineKeyboardButton(text='🚁 Лететь ещё раз', switch_inline_query_current_chat='Вертолёт лететь'))
