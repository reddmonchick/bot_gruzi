import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from curl_cffi import requests
import schedule
import time



# Загрузка учетных данных и настройка клиента
crede = {
  "type": "service_account",
  "project_id": "wbapi-410011",
  "private_key_id": "75012e9eaa5ca3c11bbb00b44432b21265810508",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCob3HsVKY9CBt0\neBjsWUsVUS1xS4h+MzjVI7B0jZIvtkTNRZbE1qysZHTp1FVGyp2/UE10nIBhbsWN\nKim327kRfuAs4fNEtk5WgOvKbvwuzlHELub0Q/BP0NFwLlrZXgdq3Hyaj0yyO35R\nZKuL1yJJoL0m8AredvXEv+2N6jVHUDd085g48WO7SzKzH5X4S9vbEWk7bNcVLZxj\nFs9nYl3KFusU/Gz2xubBL5LvE0EfGbE7QscLYINYlOZ/HDJ/aDeEwr+pxfEwk9nh\ncf+qItwu8imFXU5DVU3OzhYIq0PE8pS9Bc3CO+nNOfOlta4vv84pGXXVkI66taiD\nyX+zPiXbAgMBAAECggEAS+o+7IeSjXtz9GCUyyHLx4XY93FVyZuIh/gX9dBBDSQX\ninVM6Nbg6Ko2T5WWAdwckTe+UUqgSknE3EUenHF5zjrjCxejr1qDoFVm8Mxo+Seg\njs2c5ocgbrjtTKR36fSJX06VEox3wvUxj7nR36tNFuZNmpkiLPZs+wqOJSJkdQkl\nIf6LZsD+ZfQaKzLrCZyAlrsnQK1bLllY6ALFpzrVW31WhI7WHwVgdQ2QUVG823DJ\nyY/+6jaPr0HQdg0Nc179bO85Ia3qAkpKkaUizrQbbnXoqca78RDnQugrXN0ydvNT\nvqw+3548EtGOMHJkPsrntc0itN0r70D6BQK9r5ax8QKBgQDbEUF6cO4AeymWWCnt\nAoV++tSi0LJLsw7mO/6fS/zkYJ37Jbw4GVQ/JRtzAZE2pddNZ7WotN1PBTwsieGz\n1HbEOUmVZx5ckQQXrmo5HJ1xgFYxdc+ah6EQ0NPKTz2BtvQXvcirTN7RP3BRs0TR\n1YcdeRnN1g74Q6plhq6NUlf83wKBgQDE1PTSP153PsrSAkV/HLXKRmL2DRZYLq/D\n/ZDifLP5Gxnlo6ogU3ErJpLs7LXMKp6uRWrl2I3C7kLn5KT6vO5/K0MIGvgLvPB9\nb/7GiXCZD9bS/KXVOTWYmhJeraeE+EJygpw7DlcnNX5TokAltx6dt+msPqvA5Nyf\njN0Tvir6hQKBgElr3iM4aDxXCxgtkleySaXGUbAD/E3sxGib4Pno0OiGDUzYV94B\ndz/2ot2Hv/Ct4pw5zyOtAqNyYLmYuMG5yth3Ttc5CW8C13lMZqOfmJEq7ziCgMMN\nBAmLxAABUN8Bv4uZewEWsXM2LOHlEIK3ayKQrPpU7Q1+OETwv93zpDPHAoGALopL\n+QqSw49NVarD0/Jt6Y4LCDK//cnMNYNXJrZlt5j43pt8NniEYbeVNgAiXEwXiQ1Q\n4Vf67QR5PWuKtt7FZbxM9TWrQNtD4eUBUOBeh1J/cRPcAjasvZBwl4JoAcDRtVG8\nrxoM8XBslkne8QwDaTd7QQbwhYOXxwH/pBNrBiECgYAqFKzYEsvJBr7YRa9kc1DR\nEltZnyaqf3UPfVt0m7JOlbN/QXWiRA2nLyqKBQd7u+P4tSo0Z0eORA46yWw824A/\nl7VtEtWadHbsuHLNXWKClnNhNuox7hp7eNsAGzhwdtQp67m7hRQvHCwWzDZDpN8M\nSGbUqtq5WD42aS6Jm68n2Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "ozon-actii@wbapi-410011.iam.gserviceaccount.com",
  "client_id": "101246842926517665509",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ozon-actii%40wbapi-410011.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}



# Указываем области видимости, которые будут использоваться
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Аутентификация и получение клиента

client = gspread.service_account_from_dict(crede)

# Открываем таблицу по названию или ID (например, '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms')
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/111Z27_sprF-vI2BKDJuAeEG4LNgE1egJZdeV_VJ5scY/edit?gid=2006624034#gid=2006624034')

# Открываем первый лист
sheet = spreadsheet.worksheet('param')

print(sheet)
all_values = sheet.get_all_values()
# Получаем все значения из листа
params = {}
for row in all_values:
    if len(row) >= 2:  # Проверяем, что в строке достаточно элементов
        if row[0] == '' and row[1] == '':
            key = row[2].strip()  # Убираем пробелы вокруг ключа
            value = row[3].strip()  # Убираем пробелы вокруг значения
        else:
            key = row[0].strip()  # Убираем пробелы вокруг ключа
            value = row[1].strip()  # Убираем пробелы вокруг значения
        params[key] = value

# Извлекаем данные в переменные
client_id = params.get('Client ID', None)
api_key = params.get('API Key', None)
x2id = params.get('X2ID', None)
x3id = params.get('X3ID', None)
x4id = params.get('X4ID', None)
x2sort = params.get('X2Sort', None)
x3sort = params.get('X3Sort', None)
x4sort = params.get('X4Sort', None)
time_off_action = params.get('TIMEOFFACTION', None)
time_on_action = params.get('TIMEONACTION', None)
time_on_night_price = params.get('TIMEONNIGHTPRICE', None)
time_off_night_price = params.get('TIMEOFFNIGHTPRICE', None)
proc_action = params.get('PROCACTION', None)
proc_min_price = params.get('PROCMINPRICE', None)
proc_old_price = params.get('PROCOLDPRICE', None)
proc_night_price = params.get('PROCNIGHTPRICE', None)

# Вывод данных для проверки
print("Client ID:", client_id)
print("API Key:", api_key)
print("X2ID:", x2id)
print("X3ID:", x3id)
print("X4ID:", x4id)
print("X2Sort:", x2sort)
print("X3Sort:", x3sort)
print("X4Sort:", x4sort)
print("TIMEOFFACTION:", time_off_action)
print("TIMEONACTION:", time_on_action)
print("TIMEONNIGHTPRICE:", time_on_night_price)
print("TIMEOFFNIGHTPRICE:", time_off_night_price)
print("PROCACTION:", proc_action)
print("PROCMINPRICE:", proc_min_price)
print("PROCOLDPRICE:", proc_old_price)
print("PROCNIGHTPRICE:", proc_night_price)
headers = {
        "Client-Id": client_id,  # Замените на ваш Client ID
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
s = requests.Session()
s.headers.update(headers)

sheet = spreadsheet.worksheet('Таблица текущих цен и акций')

def chunk_list(lst, chunk_size):
    """Разбивает список на чанки по chunk_size элементов."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]







def get_ozon_product_ids(action_type):
    url = "https://api-seller.ozon.ru/v1/actions/products"  # Пример URL для получения данных о товарах в акциях

    print(headers, action_type)
    payload = {
        "action_id": action_type,
        "limit": 100,
        "offset": 0
    }

    response = s.post(url, json=payload)
    col_pages = int(response.json().get('result', {}).get('total'))

    result = []

    for offset in range(0, col_pages + 100, 100):
        payload = {
            "action_id": action_type,
            "limit": 100,
            "offset": offset
        }
        response = s.post(url, headers=headers, json=payload)
        data = response.json()
        result.extend([item["id"] for item in data.get('result', {}).get('products', [])])

    return result


def get_ozon_articul(products: list):
    url = 'https://api-seller.ozon.ru/v2/product/info/list'
    all_offer_ids = []
    c = 1000
    # Разбиваем список products на чанки по 1000 элементов
    for chunk in chunk_list(products, 1000):
        json_data = {
            'offer_id': [],
            'product_id': chunk,
            'sku': [],
        }

        response = s.post(url, json=json_data)
        print(f'articul {response} {len(products)} | {c}')
        if response.status_code == 200:
            data = response.json()
            for item in data.get('result', {}).get('items', []):
                all_offer_ids.append(item.get('offer_id'))
        else:
            print(f"Error {response.status_code}: {response.text}")
        c += 1000

    return all_offer_ids

# Получаем ID товаров для каждой акции
x2_product_ids = get_ozon_product_ids(x2id)
x3_product_ids = get_ozon_product_ids(x3id)
x4_product_ids = get_ozon_product_ids(x4id)
x2_articul = get_ozon_articul(x2_product_ids)
x3_articul = get_ozon_articul(x3_product_ids)
x4_articul = get_ozon_articul(x4_product_ids)

print(sheet)
all_values = sheet.get_all_values()

# Записываем полученные данные обратно в таблицу
def update_sheet_with_ids(sheet, column_name, product_ids):
    all_values = sheet.get_all_values()
    col_idx = all_values[0].index(column_name) + 1
    articul_col_idx = all_values[0].index("Артикул") + 1

    # Список для batch_update
    batch_updates = []

    for row_idx, row in enumerate(all_values[1:], start=2):
        for product_id, articul in zip(product_ids[0], product_ids[1]):
            if row[articul_col_idx - 1] == articul:
                # Добавляем обновление в список
                batch_updates.append({
                    'range': f'{gspread.utils.rowcol_to_a1(row_idx, col_idx)}',
                    'values': [[product_id]]
                })

    # Выполняем batch_update
    if batch_updates:
        sheet.batch_update(batch_updates)

ranges_to_clear = ['O2:O50000', 'U2:U50000', 'AA2:AA50000']

# Очищаем указанные диапазоны
for cell_range in ranges_to_clear:
    sheet.batch_clear([cell_range])

# Пример использования
update_sheet_with_ids(sheet, "X2IDVA", [x2_product_ids, x2_articul])
update_sheet_with_ids(sheet, "X3IDVA", [x3_product_ids, x3_articul])
update_sheet_with_ids(sheet, "X4IDVA", [x4_product_ids, x4_articul])

print("Товары, включенные в акции, успешно обновлены.")

# Функция для выхода из акций
def remove_from_action(api_key, product_ids, action_type):
    url = "https://api-seller.ozon.ru/v1/actions/products/deactivate"  # Пример URL для удаления товаров из акций
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "action_id": action_type,
        "product_ids": product_ids
    }

    response = s.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print(f"Removed products from action {action_type}: {data}")

# Выход из акций по IDVA
def exit_all_actions():
    if x2_product_ids:
        remove_from_action(api_key, x2_product_ids, x2id)
    if x3_product_ids:
        remove_from_action(api_key, x3_product_ids, x3id)
    if x4_product_ids:
        remove_from_action(api_key, x4_product_ids, x4id)



# Функция для установки цен
def set_product_price(api_key, products):
    url = "https://api-seller.ozon.ru/v1/product/import/prices"  # Пример URL для обновления цены товара
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "prices": products
    }

    response = s.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print(f"Updated price for products: {data}")

# Установка ночной цены
def set_night_prices():
    for chunk in chunk_list(all_values[1:], 1000):
        lst = []
        for row in chunk:
            dct = {"auto_action_enabled": "UNKNOWN",
             "currency_code": "RUB",
             "min_price": "800",
             "offer_id": "",
             "old_price": "0",
             "price": "1448",
             "price_strategy_enabled": "UNKNOWN",
             "product_id": 1386}

            product_id = row[14] if row[14] else row[19] if row[19] else row[24] if row[24] else 0
            night_price = row[5]
            dct['price'] = night_price
            dct['product_id'] = product_id
            lst.append(dct)

        set_product_price(api_key, lst)

# Установка дневной цены
def set_day_prices():
    for chunk in chunk_list(all_values[1:], 1000):
        lst = []
        for row in chunk:
            dct = {"auto_action_enabled": "UNKNOWN",
                   "currency_code": "RUB",
                   "min_price": "800",
                   "offer_id": "",
                   "old_price": "0",
                   "price": "1448",
                   "price_strategy_enabled": "UNKNOWN",
                   "product_id": 1386}

            product_id = row[14] if row[14] else row[19] if row[19] else row[24] if row[24] else 0
            night_price = row[2]
            dct['price'] = night_price
            dct['product_id'] = product_id
            lst.append(dct)

        set_product_price(api_key, lst)

# Выполнение задач по времени
def scheduled_tasks():
    # Планируем задачи на определенное время
    schedule.every().day.at(time_off_action.replace('-', ':')).do(exit_all_actions)
    schedule.every().day.at(time_on_night_price.replace('-', ':')).do(set_night_prices)
    schedule.every().day.at(time_off_night_price.replace('-', ':')).do(set_day_prices)

    # Бесконечный цикл для выполнения запланированных задач
    while True:
        schedule.run_pending()
        time.sleep(1)


# Запуск запланированных задач
scheduled_tasks()

def get_ozon_idu(action_type):
    url = "https://api-seller.ozon.ru/v1/actions/candidates"  # Пример URL для получения данных о товарах в акциях

    print(headers, action_type)
    payload = {
        "action_id": action_type,
        "limit": 100,
        "offset": 0
    }

    response = s.post(url, json=payload)
    col_pages = int(response.json().get('result', {}).get('total'))

    result = []

    for offset in range(0, col_pages + 100, 100):
        payload = {
            "action_id": action_type,
            "limit": 100,
            "offset": offset
        }
        response = s.post(url, json=payload)
        print(offset, response)
        data = response.json()
        result.extend([item["id"] for item in data.get('result', {}).get('products', [])])

    return result

def get_prices(product_ids: list, type_price: str):
    url = "https://api-seller.ozon.ru/v4/product/info/prices"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key
    }
    prices = []
    chunk_size = 1000  # размер чанка
    c = 0

    for chunk in chunk_list(product_ids, chunk_size):

        json_data = {
            'filter': {
                'product_id': chunk,
                'visibility': 'ALL',
            },
            'last_id': '',
            'limit': 1000,
        }
        response = requests.post(url, json=json_data, headers=headers)
        print(f'prices {response} {c} | {len(product_ids)}')
        c += 1000
        if response.status_code == 200:
            data = response.json()
            for item in data["result"]['items']:
                prices.append(item.get("price", {}).get(type_price, '').split('.')[0])
        else:
            for product_id in chunk:
                pass
    return prices

x2_product_idu = get_ozon_idu(x2id)
x3_product_idu = get_ozon_idu(x3id)
x4_product_idu = get_ozon_idu(x4id)
x2_articul_idu = get_ozon_articul(x2_product_idu)
x3_articul_idu = get_ozon_articul(x3_product_idu)
x4_articul_idu = get_ozon_articul(x4_product_idu)
x2_price = get_prices(x2_product_idu, 'marketing_price')
x3_price = get_prices(x3_product_idu, 'marketing_price')
x4_price = get_prices(x4_product_idu, 'marketing_price')

def update_sheet_with_prices(sheet, column_name, product_ids):
    all_values = sheet.get_all_values()
    if column_name == 'X2IDU':
        price_column_name = 'X2PRICE'
    elif column_name == 'X3IDU':
        price_column_name = 'X3PRICE'
    elif column_name == 'X4IDU':
        price_column_name = 'X4PRICE'
    else:
        raise ValueError("Unknown column name")

    col_idx = all_values[0].index(column_name) + 1
    price_col_idx = all_values[0].index(price_column_name) + 1
    articul_col_idx = all_values[0].index("Артикул") + 1

    # Список для batch_update
    batch_updates = []

    for row_idx, row in enumerate(all_values[1:], start=2):
        for product_id, articul, price in zip(product_ids[0], product_ids[1], product_ids[2]):
            if row[articul_col_idx - 1] == articul:
                # Добавляем обновление для идентификатора
                batch_updates.append({
                    'range': f'{gspread.utils.rowcol_to_a1(row_idx, col_idx)}',
                    'values': [[product_id]]
                })
                # Добавляем обновление для цены
                batch_updates.append({
                    'range': f'{gspread.utils.rowcol_to_a1(row_idx, price_col_idx)}',
                    'values': [[price]]
                })

    # Выполняем batch_update
    if batch_updates:
        sheet.batch_update(batch_updates)

print(x2_price)

ranges_to_clear = ['N2:N50000', 'T2:T50000', 'Z2:Z50000']

# Очищаем указанные диапазоны
for cell_range in ranges_to_clear:
    sheet.batch_clear([cell_range])


update_sheet_with_prices(sheet, "X2IDU", [x2_product_idu, x2_articul_idu, x2_price])
update_sheet_with_prices(sheet, "X3IDU", [x3_product_idu, x3_articul_idu, x3_price])
update_sheet_with_prices(sheet, "X4IDU", [x4_product_idu, x4_articul_idu, x4_price])


# тут мы должны вступить в акции


def update_sheet_with_ids(sheet, column_name, product_ids):
    all_values = sheet.get_all_values()
    col_idx = all_values[0].index(column_name) + 1
    articul_col_idx = all_values[0].index("Артикул") + 1


    # Список для batch_update
    batch_updates = []

    for row_idx, row in enumerate(all_values[1:], start=2):
        for product_id, articul in zip(product_ids[0], product_ids[1]):
            if row[articul_col_idx - 1] == articul:
                # Добавляем обновление в список
                batch_updates.append({
                    'range': f'{gspread.utils.rowcol_to_a1(row_idx, col_idx)}',
                    'values': [[product_id]]
                })



    # Выполняем batch_update
    if batch_updates:
        sheet.batch_update(batch_updates)

x2_product_ids = get_ozon_product_ids(x2id)
x3_product_ids = get_ozon_product_ids(x3id)
x4_product_ids = get_ozon_product_ids(x4id)
x2_articul = get_ozon_articul(x2_product_ids)
x3_articul = get_ozon_articul(x3_product_ids)
x4_articul = get_ozon_articul(x4_product_ids)

update_sheet_with_ids(sheet, "X2IDVA", [x2_product_ids, x2_articul])
update_sheet_with_ids(sheet, "X3IDVA", [x3_product_ids, x3_articul])
update_sheet_with_ids(sheet, "X4IDVA", [x4_product_ids, x4_articul])

column_o = sheet.col_values(15)  # столбец O (15 столбец в таблице)
column_t = sheet.col_values(21)  # столбец T (20 столбец в таблице)
column_y = sheet.col_values(27)  # столбец Y (25 столбец в таблице)

ranges_to_clear = ['M2:M50000']

# Очищаем указанные диапазоны
for cell_range in ranges_to_clear:
    sheet.batch_clear([cell_range])


# Проходимся по каждой строке, начиная с второй (первая строка обычно заголовок)
for i in range(2, len(column_o) + 1):
    if column_o[i - 1].strip().isdigit():
        sheet.update_cell(i, 13, 'X2')  # столбец M (13 столбец в таблице)
    if column_t[i - 1].strip().isdigit():
        sheet.update_cell(i, 13, 'X3')  # столбец M (13 столбец в таблице)
    if column_y[i - 1].strip().isdigit():
        sheet.update_cell(i, 13, 'X4')  # столбец M (13 столбец в таблице)
    else:
        sheet.update_cell(i, 13, 'Нет акции')  # столбец M (13 столбец в таблице)



def get_prices_current(products: list):
    url = 'https://api-seller.ozon.ru/v2/product/info/list'
    all_offer_ids = []
    c = 1
    # Разбиваем список products на чанки по 1000 элементов
    for chunk in chunk_list(products, 1):
        json_data = {
            'offer_id': [],
            'product_id': [],
            'sku': chunk,
        }

        response = s.post(url, json=json_data)
        print(f'price current {response} {len(products)} | {c}')
        if response.status_code == 200:
            data = response.json()
            for item in data.get('result', {}).get('items', []):
                all_offer_ids.append(item.get('price', '0').split('.')[0])
        else:
            print(f"Error {response.status_code}: {response.text}")
        c += 1

    return all_offer_ids

ranges_to_clear = ['D2:D50000']

# Очищаем указанные диапазоны
for cell_range in ranges_to_clear:
    sheet.batch_clear([cell_range])

lst = sheet.col_values(2)

print(lst)

prices = get_prices_current(lst)

column_c_values = [[value] for value in prices]

# Определяем диапазон для записи в столбец C
cell_list = sheet.range(f'D2:D{len(column_c_values)}')

# Заполняем значения в cell_list
for i, cell in enumerate(cell_list):
    cell.value = column_c_values[i][0]

# Обновляем значения в Google Sheets
sheet.update_cells(cell_list)



