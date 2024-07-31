import gspread
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

    result_id = []
    result_price = []

    for offset in range(0, col_pages + 100, 100):
        payload = {
            "action_id": action_type,
            "limit": 100,
            "offset": offset
        }
        response = s.post(url, json=payload)
        print(offset, response)
        data = response.json()
        result_id.extend([item["id"] for item in data.get('result', {}).get('products', [])])
        result_price.extend([item["action_price"] for item in data.get('result', {}).get('products', [])])
    return result_id, result_price



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


x2_id, x2_price = get_ozon_idu(x2id)
x3_id, x3_price = get_ozon_idu(x3id)
x4_id, x4_price = get_ozon_idu(x4id)
x2_articul_idu = get_ozon_articul(x2_id)
x3_articul_idu = get_ozon_articul(x3_id)
x4_articul_idu = get_ozon_articul(x4_id)
x2_price = x2_price
x3_price = x3_price
x4_price = x4_price
x4_product_idu = x4_id
x3_product_idu = x3_id
x2_product_idu = x2_id


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


ranges_to_clear = ['P2:P50000', 'V2:V50000', 'AB2:AB50000']

# Очищаем указанные диапазоны
for cell_range in ranges_to_clear:
    sheet.batch_clear([cell_range])

print('Обновляем X2PRICE')
update_sheet_with_prices(sheet, "X2IDU", [x2_product_idu, x2_articul_idu, x2_price])
print('Обновляем X3PRICE')
update_sheet_with_prices(sheet, "X3IDU", [x3_product_idu, x3_articul_idu, x3_price])
print('Обновляем X4PRICE')
update_sheet_with_prices(sheet, "X4IDU", [x4_product_idu, x4_articul_idu, x4_price])


