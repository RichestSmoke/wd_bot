from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


buy_b = KeyboardButton('🏠 Купівля')
rent_b = KeyboardButton('🏘️ Оренда')
international_b = KeyboardButton('🏠🌍 Закордонна нерухомість')
main_keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard_client.add(buy_b).add(rent_b).add(international_b)


back_button = KeyboardButton("⬅️ Повернутись")

get_contact_b = KeyboardButton("📞 Поділитись контактом", request_contact=True)
get_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(get_contact_b).add(back_button)


housing_rental = KeyboardButton('🏠 Оренда житла')
commercial_rental = KeyboardButton('🏢 Оренда комерції')
land_rental = KeyboardButton('🏞 Оренда землі')
rental_keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
rental_keyboard_client.add(housing_rental, commercial_rental, land_rental).add(back_button)
# rental_keyboard_client.add(housing_rental).add(commercial_rental).add(land_rental).add(back_button)


house_buy_b = KeyboardButton('🏠 Купівля житла')
commerce_buy_b = KeyboardButton('🏢 Купівля комерції')
land_buy_b = KeyboardButton('🏞 Купівля землі')
buy_keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
buy_keyboard_client.add(house_buy_b, commerce_buy_b, land_buy_b).add(back_button)
# buy_keyboard_client.add(house_buy_b).add(commerce_buy_b).add(land_buy_b).add(back_button)


new_hous_b = KeyboardButton('🏗️ Новобудови')
old_hous_b = KeyboardButton('🏘️ Вторинка')
house_buy_keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
house_buy_keyboard_client.add(new_hous_b, old_hous_b).add(back_button)
# house_buy_keyboard_client.add(new_hous_b).add(old_hous_b).add(back_button)