# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

def get_sheet():
    # 구글 시트 연결 함수
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('key.json', scopes=scope)
    client = gspread.authorize(creds)
    # 파일 이름이 정확해야 합니다.
    spreadsheet = client.open("chatbot_db")
    return spreadsheet.get_worksheet(0) # 첫 번째 탭을 무조건 가져옴

@app.route('/ask', methods=['POST'])
def ask():
    req = request.get_json()
    user_input = req['userRequest']['utterance'].strip()

    try:
        sheet = get_sheet() # 요청이 올 때마다 시트 연결 확인

        # 1. 추가 기능
        if user_input.startswith("추가"):
            parts = user_input.split(" ", 2)
            if len(parts) < 3:
                answer = "'추가 지역명 주소' 형식으로 입력해주세요."
            else:
                new_region = parts[1]
                new_address = parts[2]
                sheet.append_row([new_region, new_address])
                answer = f"✅ {new_region} 등록 성공 (시트 확인 요망)"

        # 2. 검색 기능
        else:
            cell = sheet.find(user_input)
            if cell:
                answer = sheet.cell(cell.row, 2).value
            else:
                answer = f"'{user_input}'은(는) 시트에 등록되어 있지 않습니다."

    except Exception as e:
        # 에러 발생 시 카톡으로 에러 내용을 직접 보냅니다.
        answer = f"⚠️ 오류 발생: {str(e)}"

    res = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
