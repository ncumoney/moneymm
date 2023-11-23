import gspread
from oauth2client.service_account import ServiceAccountCredentials

def income(spreadsheet_name, data):
    # 定義認證範圍
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # 添加您的 JSON 憑證文件
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\yunyu\Desktop\moneymm\steam-boulevard-405907-f1cc6b42920f.json', scope)
    
    # 授權和建立客戶端
    client = gspread.authorize(creds)

    # 打開 spreadsheet
    sheet = client.open(spreadsheet_name).sheet1

    # 插入數據
    sheet.append_row(data)

# 要添加的數據，例如 ["2023/03/01", "餐廳", 300]
data = ["2023/03/01", "餐廳", 300]

# Spreadsheet 名稱
spreadsheet_name = "ncummmoney"

# 呼叫函數添加數據
income(spreadsheet_name, data)