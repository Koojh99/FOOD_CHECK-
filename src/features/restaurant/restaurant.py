
# src/features/restaurant/restaurant.py
from . import maps_api

def recommend_restaurants(food_name, location):
    """특정 음식과 위치를 기반으로 음식점을 추천하는 함수"""
    try:
        query = f"{food_name} near {location}"
        places_data = maps_api.search_places(query)

        if places_data.get('results'):
            # 상위 3개 음식점을 추천 메시지로 가공
            top_3_places = places_data['results'][:3]
            message = f"'{location}' 근처 '{food_name}' 맛집 추천!\n\n"
            for i, place in enumerate(top_3_places):
                message += f"{i+1}. {place['name']}\n"
                message += f"   - 주소: {place['formatted_address']}\n"
                message += f"   - 평점: {place.get('rating', 'N/A')}\n"
            return message
        else:
            return f"'{location}' 근처에서 '{food_name}' 맛집을 찾지 못했습니다."

    except Exception as e:
        print(f"음식점 추천 중 오류 발생: {e}")
        return "음식점을 추천하는 데 실패했습니다."

