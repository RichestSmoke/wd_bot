from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import bot, MenuStates
from config import admin, managers
from keyboards import main_menu_kb, main_keyboard_client, exit_admin_kb, customer_report_kb
from collections import deque as dq
from data_base.sqlite_db import get_sql_report
from openpyxl import Workbook
import re


class AdminStates(StatesGroup):
    MAIN_MENU = State()
    ADD_CHOOSE_CATEGORY = State()
    ADD_ENTER_MANAGER_ID = State()

    DEL_CHOOSE_CATEGORY = State()
    DEL_ENTER_MANAGER_ID = State()

    DEL_ALL_MANAGER_ID = State()
    APPEND_DEL_ALL_MANAGER_ID = State()

    GET_CUSTOMER_REPORT = State()


wellcome_text = """Добро пожаловать в админ панель!
                    \nЗдесь вы можете назначить менеджера на определенную категрию.
                    \n❗️Что бы добавить менеджера нужно вписать его ID в выбранной категории. ID можно получить в боте @getmyid_bot
                    \n❗️Что бы менеджер корректно добавился он должен сначала написать боту команду '/start', только после этого можно добавлять ID менеджера!"""


def validate_manager_id(manager_id):
    pattern = r"^\d{8,10}$"
    return bool(re.match(pattern, manager_id))


async def handle_admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id in admin:
        await message.answer(wellcome_text, reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)
    else:
        await message.answer("Нет доступа!", reply_markup=main_keyboard_client)


async def add_manager_handler(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*managers.keys()).add('Выйти в Admin меню')
    await message.answer("В какую категорию добавить менеджера?", reply_markup=keyboard)
    await state.set_state(AdminStates.ADD_CHOOSE_CATEGORY)


async def enter_manager_id_handler(message: types.Message, state: FSMContext):
    category = message.text
    if category in managers:
        await state.update_data(category=category)  # Сохраняем выбранную категорию в состояние
        await message.answer("Введите ID менеджера:", reply_markup=exit_admin_kb)
        await state.set_state(AdminStates.ADD_ENTER_MANAGER_ID)

    elif category == 'Выйти в Admin меню':
        await state.finish()
        await message.answer('Выберете что вас интересует:', reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)
    else:
        await message.answer('Нет такой команды')


async def save_manager_id_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')
    manager_id = message.text
    if validate_manager_id(manager_id):
        try:
            if int(manager_id) not in managers[category]:
                await bot.send_message(int(manager_id), f"Теперь вы менеджер категории {category}, вам будут приходить контактные данные новых клиентов!")
                managers[category].append(int(manager_id))
                await message.answer(f"ID менеджера успешно добавлен для категории {category}", reply_markup=main_menu_kb)
                await state.finish()
                await state.set_state(AdminStates.MAIN_MENU)
            else:
                await message.answer(f"Этот ID уже был добавлен в список менеджеров!\nВведите другой ID или нажмите кномпу 'Выйти в Admin меню'")

        except:
            await message.answer(f"Ошибка!\nПроверьте правильность ID менеджера\nБудущий менеджер должен заранее написать боту команду '/start'")

    elif manager_id == 'Выйти в Admin меню':
        await state.finish()
        await message.answer("Вы в Admin меню!", reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)

    else:
        await message.answer(f"Ошибка!\nID не прошел валидацию\nПроверьте правильность ID менеджера")


async def show_managers_handler(message: types.Message, state: FSMContext):
    managers_string = "\n\n".join([f"{key} : {list(value)}" for key, value in managers.items()])
    await message.answer(managers_string, reply_markup=main_menu_kb)
    await state.set_state(AdminStates.MAIN_MENU)


async def del_manager_handler(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*managers.keys()).add('Выйти в Admin меню')
    await message.answer("Выберете категорию с которой хотите удалить менеджера:", reply_markup=keyboard)
    await state.set_state(AdminStates.DEL_CHOOSE_CATEGORY)


async def del_enter_manager_id(message: types.Message, state: FSMContext):
    category = message.text
    if category in managers:
        await state.update_data(category=category)  # Сохраняем выбранную категорию в состояние
        await message.answer("Введите ID менеджера:", reply_markup=exit_admin_kb)
        await state.set_state(AdminStates.DEL_ENTER_MANAGER_ID)

    elif category == 'Выйти в Admin меню':
        await state.finish()
        await message.answer('Выберете что вас интересует:', reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)
    else:
        await message.answer('Нет такой команды')


async def del_manager_id_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')
    manager_id = message.text

    if manager_id == 'Выйти в Admin меню':
        await state.finish()
        await message.answer('Выберете что вас интересует:', reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)
    
    elif manager_id.isdigit():  # Проверяем, является ли строка числом
        manager_id_int = int(manager_id) 
        if manager_id_int in managers[category]:
            managers[category].remove(manager_id_int)
            await message.answer(f"Менеджер {manager_id_int} с категории {category} удален!", reply_markup=main_menu_kb)
            await state.finish()
            await state.set_state(AdminStates.MAIN_MENU)
        else:
            await message.answer('Такого айди нет в списке менеджеров')
    else:
        await message.answer('Нет такой команды или телеграм айди неправильный')  
   

async def del_all_managers_handler(message: types.Message, state: FSMContext):
    await message.answer('Вы точно хотите удалить всех менеджеров?\nДля подтверждения отправьте боту: del_all_managers', reply_markup=exit_admin_kb)
    await state.set_state(AdminStates.APPEND_DEL_ALL_MANAGER_ID)


async def process_del_all_managers_handler(message: types.Message, state: FSMContext):
    for key in managers:
        managers[key] = dq()
    await message.answer("Вы успешно удалили всех менеджеров!", reply_markup=main_menu_kb)
    await state.set_state(AdminStates.MAIN_MENU)


async def get_customer_report_handler(message: types.Message, state: FSMContext):
    await message.answer("Выберете за какой период сделать отчет", reply_markup=customer_report_kb)
    await state.set_state(AdminStates.GET_CUSTOMER_REPORT)


async def choose_timeframe_get_customer_report_handler(message: types.Message, state: FSMContext):
    key_time = message.text
    data_sql_query = {
        'Две недели' : "SELECT * FROM clients WHERE Date >= date('now', '-14 day')",
        'Месяц' : "SELECT * FROM clients WHERE Date >= date('now', '-30 day')",
        'Три месяца' : "SELECT * FROM clients WHERE Date >= date('now', '-90 day')",
        'За все время' : "SELECT * FROM clients"
    }
    if key_time in data_sql_query:
        customer_report = await get_sql_report(data_sql_query[key_time])
        wb = Workbook()
        ws = wb.active
        ws.append(["Date", "Name", "User_id", "Phone_number", "User_name", "Category", "Manager"])
        
        for row in customer_report:  # Добавление данных в файл Excel
            ws.append(row)

        wb.save('customer_report.xlsx')
        with open('customer_report.xlsx', 'rb') as excel_file:            
            await message.answer_document(excel_file)
    
    elif key_time == 'Выйти в Admin меню':
        await message.answer('Выберете что вас интересует:', reply_markup=main_menu_kb)
        await state.set_state(AdminStates.MAIN_MENU)
    
    else:
        await message.answer('Нет такой команды!')


async def exit_in_admin_main_menu_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберете что вас интересует:', reply_markup=main_menu_kb)
    await state.set_state(AdminStates.MAIN_MENU)


async def exit_in_main_menu_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберете что вас интересует:', reply_markup=main_keyboard_client)
    await state.set_state(MenuStates.MAIN_MENU)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(handle_admin_command, commands=['admin'], state='*')

    dp.register_message_handler(add_manager_handler, lambda message: message.text == 'Добавить менеджера', state=AdminStates.MAIN_MENU.state)
    dp.register_message_handler(enter_manager_id_handler, state=AdminStates.ADD_CHOOSE_CATEGORY.state)
    dp.register_message_handler(save_manager_id_handler, state=AdminStates.ADD_ENTER_MANAGER_ID.state)

    dp.register_message_handler(show_managers_handler, lambda message: message.text == 'Показать всех менеджеров', state=AdminStates.MAIN_MENU.state)

    dp.register_message_handler(del_manager_handler, lambda message: message.text == 'Удалить менеджера', state=AdminStates.MAIN_MENU.state)
    dp.register_message_handler(del_enter_manager_id, state=AdminStates.DEL_CHOOSE_CATEGORY.state)
    dp.register_message_handler(del_manager_id_handler, state=AdminStates.DEL_ENTER_MANAGER_ID.state)

    dp.register_message_handler(del_all_managers_handler, lambda message: message.text == 'Удалить всех менеджеров', state=AdminStates.MAIN_MENU.state)
    dp.register_message_handler(process_del_all_managers_handler, lambda message: message.text == 'del_all_managers', state=AdminStates.APPEND_DEL_ALL_MANAGER_ID.state)

    dp.register_message_handler(get_customer_report_handler, lambda message: message.text == 'Отправить отчет', state=AdminStates.MAIN_MENU.state)
    dp.register_message_handler(choose_timeframe_get_customer_report_handler, state=AdminStates.GET_CUSTOMER_REPORT.state)

    dp.register_message_handler(exit_in_admin_main_menu_handler, lambda message: message.text == 'Выйти в Admin меню', state=[AdminStates.APPEND_DEL_ALL_MANAGER_ID.state, 
                                                                                                                        AdminStates.DEL_CHOOSE_CATEGORY.state,
                                                                                                                        AdminStates.ADD_CHOOSE_CATEGORY.state])
    
    dp.register_message_handler(exit_in_main_menu_handler, lambda message: message.text == 'Выйти в главное меню', state='*')