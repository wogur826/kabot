# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

# 처음 기본 정보 (서버가 켜질 때 초기화됨)
my_info = {
    "안동": "안동하회마을 안동읍 471-9",
    "서울": "서울특별시 중구 세종대로 110"
}

@app.route('/ask', methods=['POST'])
def ask():
    req = request.get_json()
    user_input = req['userRequest']['utterance'].strip() # 사용자가 보낸 메시지
    
    # 1. "추가" 기능 구현
    if user_input.startswith("추가"):
        try:
            # "추가 대구 주소..." -> ["추가", "대구", "주소..."] 로 나눔
            parts = user_input.split(" ", 2) 
            if len(parts) < 3:
                answer = "'추가 지역명 주소' 형식으로 입력해주세요."
            else:
                new_region = parts[1] # 대구
                new_address = parts[2] # 대구광역시 달서구...
                my_info[new_region] = new_address # 메모리에 저장
                answer = f"✅ {new_region} 주소가 등록되었습니다!"
        except Exception as e:
            answer = "등록 중 오류가 발생했습니다."

    # 2. 기존 검색 기능
    else:
        answer = my_info.get(user_input, "등록된 정보가 없습니다.")

    # 카카오톡 응답 형식
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
