import gspread
from oauth2client.service_account import ServiceAccountCredentials

def count(spreadsheet_name, category, data): ##data=使用者輸入的金額 category==類別
    # 定義認證範圍
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # 添加您的 JSON 憑證文件
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-boulevard-405907-f1cc6b42920f.json', scope)
    # 授權和建立客戶端
    client = gspread.authorize(creds)
    # 打開 spreadsheet
    sheet = client.open(spreadsheet_name).sheet1

    # 插入數據
    sheet.append_row([category, data])
    allcount =sheet.col_values(2)
    totocount = sum(float(value) for value in allcount if value)

    return totocount

# 要添加的數據，例如 ["2023/03/01", "餐廳", 300]
data =300 ##測試而已可刪==使用者輸入的金額 
category="飲食" ##測試而已可刪==使用者輸入的類別
# Spreadsheet 名稱
spreadsheet_name = "ncummmoney" ###要放到main

# 呼叫函數添加數據
count(spreadsheet_name, category, data) ####main


