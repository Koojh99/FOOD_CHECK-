
# src/features/diet/fatsecret_api.py
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

FATSECRET_API_KEY = os.getenv("FATSECRET_API_KEY")
FATSECRET_API_SECRET = os.getenv("FATSECRET_API_SECRET")

access_token = None

def get_access_token():
    """FatSecret API OAuth 2.0 액세스 토큰을 발급받는 함수"""
    global access_token
    if access_token:
        return access_token

    print("FatSecret API: 새로운 액세스 토큰 발급 요청...")
    try:
        auth_str = f"{FATSECRET_API_KEY}:{FATSECRET_API_SECRET}"
        auth_bytes = auth_str.encode('utf-8')
        auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

        response = requests.post(
            "https://oauth.fatsecret.com/connect/token",
            data="grant_type=client_credentials&scope=basic", # basic 스코프로 변경
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_b64}"
            }
        )
        response.raise_for_status()
        data = response.json()
        access_token = data.get("access_token")
        print("FatSecret API: 액세스 토큰 발급 성공!")
        return access_token
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if e.response else str(e)
        print(f"FatSecret API 액세스 토큰 발급 오류: {error_data}")
        raise Exception("Failed to get FatSecret access token.")

def search_food(food_name):
    """음식 이름으로 영양 정보를 검색하는 함수"""
    try:
        token = get_access_token()
        print(f"FatSecret API: '{food_name}' 음식 정보 검색 요청...")
        response = requests.post(
            "https://platform.fatsecret.com/rest/server.api",
            params={
                "method": "foods.search",
                "search_expression": food_name,
                "format": "json"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        print("FatSecret API: 음식 정보 검색 성공!")
        return response.json()
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if e.response else str(e)
        print(f"FatSecret 음식 검색 API 호출 오류: {error_data}")
        raise Exception("Failed to search food with FatSecret API.")

def search_recipe(query):
    """키워드로 레시피를 검색하는 함수"""
    try:
        token = get_access_token()
        print(f"FatSecret API: '{query}' 레시피 검색 요청...")
        response = requests.post(
            "https://platform.fatsecret.com/rest/server.api",
            params={
                "method": "recipes.search",
                "search_expression": query,
                "format": "json"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        print("FatSecret API: 레시피 검색 성공!")
        return response.json()
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if e.response else str(e)
        print(f"FatSecret 레시피 검색 API 호출 오류: {error_data}")
        raise Exception("Failed to search recipe with FatSecret API.")

def get_recipe_details(recipe_id):
    """레시피 ID로 상세 정보를 가져오는 함수"""
    try:
        token = get_access_token()
        print(f"FatSecret API: 레시피 ID '{recipe_id}' 상세 정보 요청...")
        response = requests.post(
            "https://platform.fatsecret.com/rest/server.api",
            params={
                "method": "recipe.get",
                "recipe_id": recipe_id,
                "format": "json"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        print("FatSecret API: 레시피 상세 정보 조회 성공!")
        return response.json()
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if e.response else str(e)
        print(f"FatSecret 레시피 상세 정보 API 호출 오류: {error_data}")
        raise Exception("Failed to get recipe details with FatSecret API.")
