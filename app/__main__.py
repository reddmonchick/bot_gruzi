import telebot
from telebot import types
import sqlite3

from .parsers import AtiSu

# Вставьте сюда ваш токен
API_TOKEN = '6941556547:AAFJ8CXePmDrd_CpfX7xUty294cdQqkXcBE'

bot = telebot.TeleBot(API_TOKEN)

# Соединение с базой данных
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id INTEGER PRIMARY KEY,
        data_type TEXT,
        route TEXT,
        cargo_name TEXT,
        transport_type TEXT
    )
''')

# Создание таблицы для хранения состояния пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        state TEXT,
        point_a TEXT,
        point_b TEXT,
        transport_type TEXT
    )
''')
conn.commit()


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Добро пожаловать! Я бот для сбора информации о грузах и транспорте.\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом и увидеть это сообщение\n"
        "/cancel - Отменить текущее действие и вернуться к главному меню\n"
        "/info - Получить собранную информацию\n\n"
        "Выберите одну из опций ниже, чтобы начать сбор информации:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())


# Команда /cancel
@bot.message_handler(commands=['cancel'])
def cancel_action(message):
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (message.chat.id,))
    conn.commit()
    bot.send_message(message.chat.id, "Действие отменено. Выберите опцию:", reply_markup=get_main_menu())


# Команда /info
@bot.message_handler(commands=['info'])
def send_info(message):
    cursor.execute('''
        SELECT data_type, route, cargo_name, transport_type 
        FROM user_data WHERE user_id = ?
    ''', (message.chat.id,))
    data = cursor.fetchone()

    if data:
        data_type, route, cargo_name, transport_type = data
        info_text = (
            f"Тип данных: {data_type}\n"
            f"Маршрут: {route}\n"
            f"Наименование груза: {cargo_name}\n"
            f"Тип транспортного средства: {transport_type}"
        )
    else:
        info_text = "Нет данных для отображения."

    bot.send_message(message.chat.id, info_text)


# Возвращает главное меню
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Парсинг груза")
    item2 = types.KeyboardButton("Парсинг транспорта")
    item3 = types.KeyboardButton("/cancel")
    markup.add(item1, item2, item3)
    return markup


# Обработка выбора
@bot.message_handler(func=lambda message: message.text in ["Парсинг груза", "Парсинг транспорта"])
def gather_information(message):
    if message.text == "Парсинг груза":
        cursor.execute('''
            INSERT OR REPLACE INTO user_states (user_id, state)
            VALUES (?, ?)
        ''', (message.chat.id, 'get_point_a'))
        conn.commit()
        bot.send_message(message.chat.id, "Введите пункт А:")
        bot.register_next_step_handler(message, get_point_a)
    else:
        cursor.execute('''
            INSERT OR REPLACE INTO user_states (user_id, state)
            VALUES (?, ?)
        ''', (message.chat.id, 'get_transport_type'))
        conn.commit()
        bot.send_message(message.chat.id, "Введите вид транспорта:")
        bot.register_next_step_handler(message, get_transport_type)


def get_point_a(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_states
        SET point_a = ?, state = 'get_point_b'
        WHERE user_id = ?
    ''', (message.text, message.chat.id))
    conn.commit()
    bot.send_message(message.chat.id, "Введите пункт Б:")
    bot.register_next_step_handler(message, get_point_b)


def get_point_b(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_states
        SET point_b = ?, state = 'get_cargo_name'
        WHERE user_id = ?
    ''', (message.text, message.chat.id))
    conn.commit()

    cursor.execute('''
        SELECT point_a, point_b FROM user_states WHERE user_id = ?
    ''', (message.chat.id,))
    row = cursor.fetchone()
    route = f"{row[0]} - {row[1]}"

    cursor.execute('''
        INSERT OR REPLACE INTO user_data (user_id, data_type, route)
        VALUES (?, ?, ?)
    ''', (message.chat.id, 'cargo', route))
    conn.commit()

    bot.send_message(message.chat.id, "Введите наименование груза:")
    bot.register_next_step_handler(message, get_cargo_name)


def get_cargo_name(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_data
        SET cargo_name = ?
        WHERE user_id = ? AND data_type = 'cargo'
    ''', (message.text, message.chat.id))
    conn.commit()

    bot.send_message(message.chat.id, "Введите вид транспортного средства:")
    bot.register_next_step_handler(message, get_transport_type_cargo)


def get_transport_type_cargo(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_data
        SET transport_type = ?
        WHERE user_id = ? AND data_type = 'cargo'
    ''', (message.text, message.chat.id))
    conn.commit()

    finalize_data_collection(message)


def get_transport_type(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_states
        SET transport_type = ?, state = 'get_transport_point_a'
        WHERE user_id = ?
    ''', (message.text, message.chat.id))
    conn.commit()
    bot.send_message(message.chat.id, "Введите наименование груза:")
    bot.register_next_step_handler(message, get_cargo_name_transport)


def get_cargo_name_transport(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_data
        SET cargo_name = ?
        WHERE user_id = ? AND data_type = 'transport'
    ''', (message.text, message.chat.id))
    conn.commit()

    bot.send_message(message.chat.id, "Введите пункт А:")
    bot.register_next_step_handler(message, get_transport_point_a)


def get_transport_point_a(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_states
        SET point_a = ?, state = 'get_transport_point_b'
        WHERE user_id = ?
    ''', (message.text, message.chat.id))
    conn.commit()
    bot.send_message(message.chat.id, "Введите пункт Б:")
    bot.register_next_step_handler(message, get_transport_point_b)


def get_transport_point_b(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_states
        SET point_b = ?, state = NULL
        WHERE user_id = ?
    ''', (message.text, message.chat.id))
    conn.commit()

    cursor.execute('''
        SELECT point_a, point_b, transport_type FROM user_states WHERE user_id = ?
    ''', (message.chat.id,))
    row = cursor.fetchone()
    route = f"{row[0]} - {row[1]}"
    transport_type = row[2]

    cursor.execute('''
        INSERT OR REPLACE INTO user_data (user_id, data_type, route, transport_type)
        VALUES (?, ?, ?, ?)
    ''', (message.chat.id, 'transport', route, transport_type))
    conn.commit()

    finalize_data_collection(message)


def finalize_data_collection(message):
    bot.send_message(message.chat.id, "Спасибо! Информация собрана.")
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (message.chat.id,))
    conn.commit()

    cursor.execute('''
        SELECT data_type, route, cargo_name, transport_type 
        FROM user_data WHERE user_id = ?
    ''', (message.chat.id,))
    data = cursor.fetchone()

    if data:
        data_type, route, cargo_name, transport_type = data
        print(f"Данные собраны:\nТип данных: {data_type}\nМаршрут: {route}\nНаименование груза: {cargo_name}\nТип транспортного средства: {transport_type}")

        a = route.split('-')[0]
        b = route.split('-')[-1]
        atisik = AtiSu(a, b, transport_type, cargo_name)
        if data_type == 'cargo':
            atisik.run_gruz()
        else:
            print('запустили авто')
            atisik.run_avto()

        try:
            with open('output.xlsx', 'rb') as file:
                bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, "Файл output.xlsx отправлен.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при отправке файла: {e}")

    else:
        print("Нет данных для отображения.")


bot.polling()
