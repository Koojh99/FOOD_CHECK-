
# src/features/pairing/pairing.py
from . import spoonacular_api

def recommend_pairing(food, weather, emotion):
    """음식, 날씨, 감정에 따라 음식을 추천하고 와인 페어링을 제안하는 함수"""
    try:
        # LLM을 활용하여 날씨와 감정에 기반한 추천 로직을 생성
        # (실제 구현에서는 이 부분에 LLM 호출 코드가 들어갑니다)
        recommended_food = food
        if weather == 'rainy' and emotion == 'sad':
            recommended_food = 'Pajeon (Korean Pancake)' # 예시: 추천 음식 변경

        pairing_data = spoonacular_api.get_wine_pairing(recommended_food)

        if pairing_data.get('pairedWines'):
            wine = pairing_data['pairedWines'][0]
            message = f"{weather == 'rainy' and '비 오는 날엔' or ''} '{recommended_food}' 어떠세요? 이 음식과 잘 어울리는 와인으로는 '{wine}'을 추천합니다."
            return message
        else:
            return f"'{recommended_food}'와 어울리는 와인을 찾지 못했습니다. 하지만 맛있게 드세요!"

    except Exception as e:
        print(f"페어링 추천 중 오류 발생: {e}")
        return "음식 페어링 정보를 가져오는 데 실패했습니다."
