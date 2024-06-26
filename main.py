import telebot
from telebot import types
import sqlite3

# Вставьте сюда ваш токен
API_TOKEN = '6941556547:AAFJ8CXePmDrd_CpfX7xUty294cdQqkXcBE'

bot = telebot.TeleBot(API_TOKEN)

# Соединение с базой данных
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id INTEGER,
        data_type TEXT,
        route TEXT,
        cargo_name TEXT,
        transport_type TEXT,
        vehicle TEXT
    )
''')

# Создание таблицы для хранения состояния пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        state TEXT,
        point_a TEXT,
        point_b TEXT,
        transport_type TEXT,
        vehicle TEXT
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
        "/cancel - Отменить текущее действие и вернуться к главному меню\n\n"
        "Выберите одну из опций ниже, чтобы начать сбор информации:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())


# Команда /cancel
@bot.message_handler(commands=['cancel'])
def cancel_action(message):
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (message.chat.id,))
    conn.commit()
    bot.send_message(message.chat.id, "Действие отменено. Выберите опцию:", reply_markup=get_main_menu())


# Возвращает главное меню
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Собрать информацию о грузе")
    item2 = types.KeyboardButton("Собрать информацию о транспорте")
    item3 = types.KeyboardButton("/cancel")
    markup.add(item1, item2, item3)
    return markup


# Обработка выбора
@bot.message_handler(
    func=lambda message: message.text in ["Собрать информацию о грузе", "Собрать информацию о транспорте"])
def gather_information(message):
    if message.text == "Собрать информацию о грузе":
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
        INSERT INTO user_data (user_id, data_type, route)
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
    bot.register_next_step_handler(message, get_vehicle)


def get_vehicle(message):
    if message.text == "/cancel":
        cancel_action(message)
        return

    cursor.execute('''
        UPDATE user_data
        SET vehicle = ?
        WHERE user_id = ? AND data_type = 'cargo'
    ''', (message.text, message.chat.id))
    conn.commit()

    bot.send_message(message.chat.id, "Спасибо! Информация о грузе собрана.")
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (message.chat.id,))
    conn.commit()


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
        INSERT INTO user_data (user_id, data_type, route, transport_type)
        VALUES (?, ?, ?, ?)
    ''', (message.chat.id, 'transport', route, transport_type))
    conn.commit()

    bot.send_message(message.chat.id, "Спасибо! Информация о транспорте собрана.")
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (message.chat.id,))
    conn.commit()


# Запуск бота
bot.polling(none_stop=True)
