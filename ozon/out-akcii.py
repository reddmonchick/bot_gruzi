import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from curl_cffi import requests
import schedule
import time


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

x2_product_ids = get_ozon_product_ids(x2id)
x3_product_ids = get_ozon_product_ids(x3id)
x4_product_ids = get_ozon_product_ids(x4id)
x2_articul = get_ozon_articul(x2_product_ids)
x3_articul = get_ozon_articul(x3_product_ids)
x4_articul = get_ozon_articul(x4_product_ids)



def exit_all_actions():
    if x2_product_ids:
        remove_from_action(api_key, x2_product_ids, x2id)
    if x3_product_ids:
        remove_from_action(api_key, x3_product_ids, x3id)
    if x4_product_ids:
        remove_from_action(api_key, x4_product_ids, x4id)


def scheduled_tasks():
    # Планируем задачи на определенное время
    schedule.every().day.at(time_off_action.replace('-', ':')).do(exit_all_actions)

    # Бесконечный цикл для выполнения запланированных задач
    while True:
        print(f"Ждем время для выхода из акции {time_off_action.replace('-', ':')}")
        schedule.run_pending()
        time.sleep(1)



# Запуск запланированных задач
scheduled_tasks()

