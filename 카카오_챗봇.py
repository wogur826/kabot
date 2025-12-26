# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 구글 시트 연결 설정
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('key.json', scopes=scope)
client = gspread.authorize(creds)

# 아까 만든 시트 이름 'chatbot_db'와 정확히 일치해야 합니다.
spreadsheet = client.open("chatbot_db")
sheet = spreadsheet.sheet1

@app.route('/ask', methods=['POST'])
def ask():
    req = request.get_json()
    user_input = req['userRequest']['utterance'].strip()

    # 1. 추가 기능: "추가 지역명 주소"
    if user_input.startswith("추가"):
        try:
            parts = user_input.split(" ", 2)
            if len(parts) < 3:
                answer = "'추가 지역명 주소' 형식으로 입력해주세요."
            else:
                new_region = parts[1]
                new_address = parts[2]
                # 시트 맨 아래에 새로운 줄 추가
                sheet.append_row([new_region, new_address])
                answer = f"✅ {new_region} 주소가 구글 시트에 영구 등록되었습니다!"
  except Exception as e:
        answer = f"시트 등록 실패: {str(e)}"

    # 2. 검색 기능
    else:
        try:
            # 시트의 A열에서 지역명 검색
            cell = sheet.find(user_input)
            if cell:
                # 검색된 줄의 B열(주소) 가져오기
                answer = sheet.cell(cell.row, 2).value
            else:
                answer = "등록된 정보가 없습니다."
        except:
            answer = "등록된 정보가 없습니다."

    res = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



