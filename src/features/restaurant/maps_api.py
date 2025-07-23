
# src/features/restaurant/maps_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def search_places(query):
    """특정 검색어로 주변 장소를 검색하는 함수"""
    print(f"Google Maps API: '{query}' 장소 검색 요청 시작...")
    try:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/place/textsearch/json",
            params={
                "key": GOOGLE_MAPS_API_KEY,
                "query": query,
                "language": 'ko' # 결과를 한국어로 받기
            }
        )
        response.raise_for_status()
        print("Google Maps API: 장소 검색 성공!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Google Maps API 호출 오류: {e.response.json() if e.response else e}")
        raise Exception("Failed to search places with Google Maps API.")
