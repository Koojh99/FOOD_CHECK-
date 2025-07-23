
# src/features/pairing/spoonacular_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

def get_wine_pairing(food_name):
    """특정 음식과 어울리는 와인을 추천받는 함수"""
    print(f"Spoonacular API: '{food_name}' 와인 페어링 요청 시작...")
    try:
        response = requests.get(
            "https://api.spoonacular.com/food/wine/pairing",
            params={
                "apiKey": SPOONACULAR_API_KEY,
                "food": food_name
            }
        )
        response.raise_for_status()
        print("Spoonacular API: 와인 페어링 정보 조회 성공!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Spoonacular API 호출 오류: {e.response.json() if e.response else e}")
        raise Exception("Failed to get wine pairing from Spoonacular API.")
