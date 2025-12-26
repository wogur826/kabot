
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)
# ... (이하 동일)from flask import Flask, request, jsonify

app = Flask(__name__)

# 안동 검색 시 나올 주소 설정
my_info = {
    "안동": "안동하회마을 안동읍 471-2",
    "서울": "서울특별시 중구 세종대로 110"
}

@app.route('/ask', methods=['POST'])
def ask():
    req = request.get_json()
    user_input = req['userRequest']['utterance'].strip()
    answer = my_info.get(user_input, "등록된 정보가 없습니다.")

    res = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
