import requests
from config import properties
DISCORD_TOKEN = properties.DISCORD_TOKEN
APP_ID = properties.DISCORD_APP_ID
GUILD_ID = properties.GUILD_ID  # 테스트 중엔 서버 한정 등록 추천

BASE_URL = f"https://discord.com/api/v10/applications/{APP_ID}"
HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

commands = [
    {
        "name": "help",
        "description": "명령어 목록과 설명을 확인합니다."
    },
    {
        "name": "register_goal",
        "description": "목표를 등록합니다."
    },
    {
        "name": "view_goal",
        "description": "목표 목록을 확인합니다."
    }
]

def register_commands():
    url = f"{BASE_URL}/guilds/{GUILD_ID}/commands"  # 개발/테스트 시 서버 한정 등록
    # url = f"{BASE_URL}/commands"  # 전역 등록 (실서비스 시)

    for cmd in commands:
        resp = requests.post(url, headers=HEADERS, json=cmd)
        if resp.status_code == 201:
            print(f"✅ 등록 성공: {cmd['name']}")
        else:
            print(f"⚠️ 등록 실패: {cmd['name']} - {resp.text}")
