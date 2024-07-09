import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

crede = {
  "type": "service_account",
  "project_id": "wbapi-410011",
  "private_key_id": "d4658020fa1277d4350b9393d574f8d5351e2219",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCvnOPnUW0ZsQ9Y\nuuYeXechzpq02i0XZRK3q9/Vcy18Y4PTpBs8ObaVvK0HsLiBdItI3v3z3w22/qEj\nV11SpRbmOJcYM0n/rrwFa4lQbCnzkHAgByTNMZPol7w9XvUEKAoDSGMvXg8EwjK8\n8eltqkCe+8Tjb/MXSvndda+BNlMWTiuB4m0cqN9EXEj6qYrdQuhUKFLA1ZVh9wXg\nPpuMVFQ+88jXfH3hSsRITrnt/0XXJGSkJKn8lUuQ4iM5zL0zqMw6mtrRel/08Yj9\nLUHiZaxoQIcraA37G1ZjZUbcVkpZXAcA4X2cMDo8mYPNGLh4zbAjEFRKfS0rvBGM\nug4I8ifVAgMBAAECggEAVx4mIylOTbn8CoEBSpw73pYPQlufleUCsZI2or2WGYiG\nq7XT+v8IeGTWk6OUDEiEFlzlL5d+RsMvrggXmDmk0AXP0uYSth/5T1kHEBnwf88u\nCH1ywMZxAShQ7kMOmobAXNuKtMNdAPfT0s7RhaE5mIT+qfNt7Sa5KKdKrveDpWLE\nnaOlp0qtDA67oIBIgKn6Xgp8FRVF1X7+KNDznPJwfpALrmPk0FAcTIhCUFI2ykzD\nyXecHsLsDVXsDkheH2SH9GoYHcUPbEL5yzNpnCBD340dwzX30+BHEe2nIecxYhIk\nUcdIz6RHbPVz14YECOXddUlJFP3NrP4ww/nc8JFYWwKBgQDZGkItGXdr0xnPeiLa\nLfwsYepy3BDjlFanLUOTeZt6Y8thLGrCrg+2XDce/AWT5Zuiy97OoRtr0eKFdkKU\n2FW4dtXtm/DkeuK/LIXoRVhcY6OsUJu8P9hcvGe58ZlwKm8i/FQogYyigWQ6GD8z\nrgt/pAR+UQjFN+kEKjDT0v6t0wKBgQDPE6RtzRJWaqCfzM25BRW5rKa3viylRvzp\n1i5ZDDCoDVnoYR9mLnKfDKCv8+mFTxAR0xSomAIXFV/BowQi+wfOO4rXwNA52uoV\nJkN94qkNGuSF18nTqPALk38KR9fGkBSHq6f8VecsBOMtkID4O0LVk4xu72uG0xi8\ngiJKGe7CtwKBgQCA5IsXdYAmHu269VtNx3Fo9DUaPjc0tjQACuqM2u0I68iqh5FW\nxbqEXRlIpv20weP18i305Ud/atueuwhqkEnMO5lk+Wk6bQ7Dy24w6UK9j1Z0DmN3\njzwoSp8WkS60nizfS4m3hrp1HHbh2tVjHFitTjZwvDGFzVzlYRseF62miwKBgCdj\ngxlnsp9BdQAwgsk40GMbFjNJN1DQ6fbIyNQjX3X35CwxnTlgiGj8i+wsJzU2TsY1\nMm7HS058wFQi3/yPZ3KxHL3hbTo0C+at+pSNcr6NaP6Uh019ivuIuNeJxt98NIuB\n+VgkNu7Glzfpjr6o9xONF19ap0dkDAZ/cmpJ+IKNAoGBAI6k3R0FZm/KXNVy7Hga\n9Y44VUrqMzLThZLjT2eL12yHzSlTPkCOHJosHqR6Wr9eyUsoFjLMSwfMccK/8pX6\np5d5nhZCHX2ej04ybmKgOsTSC4WX22A+f8h++kbm2uxIDAxDwSFfAHn1FfECsQez\n6WIBQOFadNeuEndzaML6r5Z5\n-----END PRIVATE KEY-----\n",
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
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/111Z27_sprF-vI2BKDJuAeEG4LNgE1egJZdeV_VJ5scY')

# Открываем первый лист
sheet = spreadsheet.worksheet('param')

print(sheet)
all_values = sheet.get_all_values()
# Получаем все значения из листа
params = {}
for row in all_values:
    print(row)
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

def get_ozon_product_ids(api_key, action_type):
    url = "https://api-seller.ozon.ru/v2/actions"  # Пример URL для получения данных о товарах в акциях
    headers = {
        "Client-Id": "your_client_id",  # Замените на ваш Client ID
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "action_type": action_type
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return [item["product_id"] for item in data["result"]]

# Извлекаем необходимые данные
api_key = all_values[1][1]  # Предполагаем, что API Key находится во второй строке второго столбца

# Получаем ID товаров для каждой акции
x2_product_ids = get_ozon_product_ids(api_key, "X2")
x3_product_ids = get_ozon_product_ids(api_key, "X3")
x4_product_ids = get_ozon_product_ids(api_key, "X4")

# Записываем полученные данные обратно в таблицу
def update_sheet_with_ids(sheet, column_name, product_ids):
    col_idx = all_values[0].index(column_name) + 1  # Номер столбца с нужным названием
    for row_idx, product_id in enumerate(product_ids, start=2):  # Начинаем со второй строки
        sheet.update_cell(row_idx, col_idx, product_id)

update_sheet_with_ids(sheet, "X2IDVA", x2_product_ids)
update_sheet_with_ids(sheet, "X3IDVA", x3_product_ids)
update_sheet_with_ids(sheet, "X4IDVA", x4_product_ids)

print("Товары, включенные в акции, успешно обновлены.")