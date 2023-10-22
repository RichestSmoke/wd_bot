from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

exit_a_b = KeyboardButton('Выйти в Admin меню')
exit_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(exit_a_b)

add_manager_b = KeyboardButton('Добавить менеджера')
show_menedgers_b = KeyboardButton('Показать всех менеджеров')
del_manager_b = KeyboardButton('Удалить менеджера')
del_all_managers_b = KeyboardButton('Удалить всех менеджеров')
customer_report = KeyboardButton('Отправить отчет')
exit_b = KeyboardButton('Выйти в главное меню')
main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_kb.add(add_manager_b, show_menedgers_b).add(del_manager_b, del_all_managers_b).add(customer_report).add(exit_b)


two_weeks_b = KeyboardButton('Две недели')
one_month_b = KeyboardButton('Месяц')
three_month_b = KeyboardButton('Три месяца')
all_report_b = KeyboardButton('За все время')
customer_report_kb = ReplyKeyboardMarkup(resize_keyboard=True)
customer_report_kb.add(two_weeks_b, one_month_b, three_month_b, all_report_b).add(exit_a_b)