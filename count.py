import gspread
from oauth2client.service_account import ServiceAccountCredentials

def count(user_id, category, data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-boulevard-405907-f1cc6b42920f.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_name = "ncummmoney"
    sheet = client.open(spreadsheet_name)
    worksheet_titles = [worksheet.title for worksheet in sheet.worksheets()]
    worksheet_name_to_check = str(user_id)

    if worksheet_name_to_check in worksheet_titles:
        personsheet=sheet.worksheet(worksheet_name_to_check)
    else:
        personsheet = sheet.add_worksheet(title=worksheet_name_to_check, rows="1000", cols="1000")

    personsheet.append_row([category, data])
    allcount =personsheet.col_values(2)
    totocount = sum(float(value) for value in allcount if value)

    maxxx=len(personsheet.col_values(1))
    records = personsheet.col_values(1)

    counttotal={}
    for i in range(maxxx):
      if records[i]=='日用品':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '日用品' in counttotal:
          counttotal['日用品']+=readwhere
        else:
          counttotal['日用品']=readwhere
        print(counttotal)
      if records[i]=='娛樂':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '娛樂' in counttotal:
          counttotal['娛樂']+=readwhere
        else:
          counttotal['娛樂']=readwhere
        print(counttotal)
      if records[i]=='交通':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '交通' in counttotal:
          counttotal['交通']+=readwhere
        else:
          counttotal['交通']=readwhere
        print(counttotal)
      if records[i]=='飲食':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '飲食' in counttotal:
          counttotal['飲食']+=readwhere
        else:
          counttotal['飲食']=readwhere
        print(counttotal)
    counttotal['餘額']=totocount

    return counttotal

data = 300
user_id='U4249cbdf64ce421b9c8e225d9260db69'
category='日用品'
category_totals= count(user_id, category, data)
reply_message = "各類別消費總額:\n" + "\n".join([f"{category}: {total}" for category, total in category_totals.items()])
print(reply_message)
#line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
