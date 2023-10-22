import sqlite3 as sq
import os


def sql_start():
    global base, cur
    base = sq.connect("clients_data_base.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute("CREATE TABLE IF NOT EXISTS clients(Date TEXT, Name TEXT, User_id TEXT, Phone_number TEXT, User_name TEXT, Category TEXT, Manager TEXT)")
    base.commit()

    #     "Date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "Name" : "message.contact.first_name",
    #     "User_id" : "message.contact.user_id",
    #     "Phone_number" : 234425454,
    #     "User_name" : "@sjhfbsfhb"

async def sql_add_row(user_info, category, manager):
    cur.execute('INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(user_info.values()) + (category,) + (manager,))
    base.commit() 

async def get_sql_report(sql_query):
    cur.execute(sql_query)
    data = cur.fetchall()
    return data

# sql_start()