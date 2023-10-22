from keyboards import main_keyboard_client, rental_keyboard_client, buy_keyboard_client, house_buy_keyboard_client, get_contact_kb
from config import managers
from create_bot import bot, MenuStates
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import Text, Command
from datetime import datetime
from data_base import sqlite_db
import aiofiles
from aiogram.utils.markdown import hlink





async def send_txt_and_get_contact(message: types.Message, state: FSMContext, property_type: str):
    text = f"Ви обрали {property_type}, залишіть, будь-ласка, свій контакт і наш менеджер з Вами зв'яжеться."
    await message.answer(text, reply_markup=get_contact_kb)


async def send_welcom(message: types.Message, state: FSMContext):
    text = 'Компанія WD Estate пропонує повний спектр послуг в сфері нерухомості від кращих експертів з багаторічним досвідом.'
    async with aiofiles.open("bot/od_estate.jpeg", "rb") as photo:
        await message.answer_photo(photo)
    await message.answer(f"Вітаємо, {message.from_user.first_name}\n{text}")
    await message.answer('Оберіть цікавий для Вас напрямок:', reply_markup=main_keyboard_client)
    await state.set_state(MenuStates.MAIN_MENU)


async def rent_handler(message: types.Message, state: FSMContext):
    await message.answer("Оберіть що ви хочете орендувати:", reply_markup=rental_keyboard_client)
    await state.set_state(MenuStates.MENU_RENT)


async def housing_rental_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "оренда житла")
    await state.set_state(MenuStates.GET_CONTACT_RENT_HOUSE) 


async def commercial_rental_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "оренда комерції")
    await state.set_state(MenuStates.GET_CONTACT_RENT_COMMERS)


async def land_rental_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "оренда землі")
    await state.set_state(MenuStates.GET_CONTACT_RENT_LAND)


async def buy_handler(message: types.Message, state: FSMContext):
    await message.answer("Оберіть що вас цікавить:", reply_markup=buy_keyboard_client)
    await state.set_state(MenuStates.MENU_BUY)


async def house_buy_handler(message: types.Message, state: FSMContext):
    await message.answer("Оберіть яке житло вас цікавить:", reply_markup=house_buy_keyboard_client)
    await state.set_state(MenuStates.MENU_BUY_HOUSE)


async def commerce_buy_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "купівля комерції")
    await state.set_state(MenuStates.GET_CONTACT_BUY_COMMERS)


async def land_buy_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "купівля землі")
    await state.set_state(MenuStates.GET_CONTACT_BUY_LAND)


async def new_hous_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "купівля новобудови")
    await state.set_state(MenuStates.GET_CONTACT_BUY_HOUSE_NEW)


async def old_hous_handler(message: types.Message, state: FSMContext):
    await send_txt_and_get_contact(message, state, "купівля вторинки")
    await state.set_state(MenuStates.GET_CONTACT_BUY_HOUSE_OLD)


async def international_real_estate_handler(message: types.Message, state:FSMContext):
    await send_txt_and_get_contact(message, state, "закордонна нерухомість")
    await state.set_state(MenuStates.GET_CONTACT_INTERNATIONAL)
    

async def contact_handler(message: types.Message, state: FSMContext):
    text_of_thanks = "Дякуємо!\nВи надіслали контакт менеджеру.\nПоки наш менеджер опрацьовує Вашу заявку, Ви можете ознайомитись з нашою діяльністю "
    # text_link = hlink('на сайті.', 'https://wd.od.ua/about/')
    text_link = "<a href='https://wd.od.ua/about/'>на сайті.</a>"

    user_info = {
        "Date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name" : message.contact.first_name,
        "User_id" : message.contact.user_id,
        "Phone_number" : message.contact.phone_number
    }
    user_info_message = f"Имя: {message.contact.first_name}\nID пользователя: {message.contact.user_id}\nНомер телефона: +{message.contact.phone_number}"
    if message.from_user.username:
        user_info["User_name"] = f"@{message.from_user.username}"
        user_info_message += f"\nИмя пользователя: @{message.from_user.username}"
    else:
        user_info["User_name"] = "Не указано!"
        user_info_message += f"\nИмя пользователя: Не указано!"

    state_to_manager = {
        MenuStates.GET_CONTACT_RENT_HOUSE.state: ["rent_house", "оренда житла"],
        MenuStates.GET_CONTACT_RENT_COMMERS.state: ["rent_commers", "оренда комерції"],
        MenuStates.GET_CONTACT_RENT_LAND.state: ["rent_land", "оренда землі"],
        MenuStates.GET_CONTACT_BUY_HOUSE_NEW.state: ["buy_house_new", "купівля новобудови"],
        MenuStates.GET_CONTACT_BUY_HOUSE_OLD.state: ["buy_house_old", "купівля вторинки"],
        MenuStates.GET_CONTACT_BUY_COMMERS.state: ["buy_commers", "купівля комерції"],
        MenuStates.GET_CONTACT_BUY_LAND.state: ["buy_land", "купівля землі"],
        MenuStates.GET_CONTACT_INTERNATIONAL.state: ["international", "закордонна нерухомість"]
    }

    current_state = await state.get_state()
    manager_key = state_to_manager.get(current_state)

    if manager_key:
        manager = managers[manager_key[0]].popleft()
        await sqlite_db.sql_add_row(user_info, category=manager_key[1].capitalize(), manager=manager)
        await bot.send_message(manager, f"{manager_key[1].capitalize()}:\n{user_info_message}")
        await message.answer(f"{text_of_thanks}{text_link}")
        managers[manager_key[0]].append(manager)


async def back_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if (current_state == MenuStates.MENU_BUY.state or current_state == MenuStates.MENU_RENT.state or current_state == None 
        or current_state == MenuStates.GET_CONTACT_INTERNATIONAL.state):
        await message.answer("Оберіть цікавий для Вас напрямок:", reply_markup=main_keyboard_client)
        await state.set_state(MenuStates.MAIN_MENU)
    elif current_state == MenuStates.MENU_BUY_HOUSE.state:
        await message.answer("Оберіть що вас цікавить:", reply_markup=buy_keyboard_client)
        await state.set_state(MenuStates.MENU_BUY)
    elif (current_state == MenuStates.GET_CONTACT_RENT_LAND.state or current_state == MenuStates.GET_CONTACT_RENT_HOUSE.state 
          or current_state == MenuStates.GET_CONTACT_RENT_COMMERS.state):
        await message.answer("Оберіть що ви хочете орендувати:", reply_markup=rental_keyboard_client)
        await state.set_state(MenuStates.MENU_RENT)
    elif current_state == MenuStates.GET_CONTACT_BUY_COMMERS.state or current_state == MenuStates.GET_CONTACT_BUY_LAND.state:
        await message.answer("Оберіть що вас цікавить:", reply_markup=buy_keyboard_client)
        await state.set_state(MenuStates.MENU_BUY)
    elif current_state == MenuStates.GET_CONTACT_BUY_HOUSE_NEW.state or current_state == MenuStates.GET_CONTACT_BUY_HOUSE_OLD.state:
        await message.answer("Оберіть яке житло вас цікавить:", reply_markup=house_buy_keyboard_client)
        await state.set_state(MenuStates.MENU_BUY_HOUSE)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(send_welcom, commands=['start'], state='*')

    dp.register_message_handler(buy_handler, lambda message: message.text == '🏠 Купівля', state=MenuStates.MAIN_MENU.state)
    dp.register_message_handler(rent_handler, lambda message: message.text == '🏘️ Оренда', state=MenuStates.MAIN_MENU.state)
    dp.register_message_handler(international_real_estate_handler, lambda message: message.text == '🏠🌍 Закордонна нерухомість', state=MenuStates.MAIN_MENU.state)

    dp.register_message_handler(housing_rental_handler, lambda message: message.text == '🏠 Оренда житла', state=MenuStates.MENU_RENT.state)
    dp.register_message_handler(commercial_rental_handler, lambda message: message.text == '🏢 Оренда комерції', state=MenuStates.MENU_RENT.state)
    dp.register_message_handler(land_rental_handler, lambda message: message.text == '🏞 Оренда землі', state=MenuStates.MENU_RENT.state)

    dp.register_message_handler(house_buy_handler, lambda message: message.text == '🏠 Купівля житла', state=MenuStates.MENU_BUY.state)
    dp.register_message_handler(commerce_buy_handler, lambda message: message.text == '🏢 Купівля комерції', state=MenuStates.MENU_BUY.state)
    dp.register_message_handler(land_buy_handler, lambda message: message.text == '🏞 Купівля землі', state=MenuStates.MENU_BUY.state)

    dp.register_message_handler(new_hous_handler, lambda message: message.text == '🏗️ Новобудови', state=MenuStates.MENU_BUY_HOUSE.state)
    dp.register_message_handler(old_hous_handler, lambda message: message.text == '🏘️ Вторинка', state=MenuStates.MENU_BUY_HOUSE.state)

    dp.register_message_handler(back_handler, lambda message: message.text == "⬅️ Повернутись", state='*')

    dp.register_message_handler(contact_handler, content_types=types.ContentType.CONTACT, state='*')


 

