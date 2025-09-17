# Discord_Chatbot_Server
discord_interactions/
├── __init__.py
├── routes.py                     # FastAPI 엔드포인트 (discord webhook entrypoint)
├── handlers/
│   ├── __init__.py
│   ├── slash_command_handlers.py # /help, /register_goal, /view_goal 등
│   ├── component_handlers.py     # 버튼 클릭 처리
│   ├── modal_handlers.py         # 입력 폼 제출 처리
├── services/
│   ├── __init__.py
│   ├── goal_api.py               # Spring REST API 호출 (목표 등록/조회/수정/삭제/스터디 시작/종료)
│   ├── utils.py                  # 공통 유틸 (요청/응답 변환 등)
