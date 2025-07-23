
# src/features/diet/diet.py
from . import fatsecret_api
import re

# 일일 권장 섭취량 (예시 데이터, 실제로는 사용자에 맞춰 개인화 필요)
DAILY_RECOMMENDATIONS = {
    'calories': 2000, # kcal
    'protein': 50,    # g
    'carbohydrate': 275, # g
    'fat': 78,      # g
}

def parse_nutrition_info(description):
    """API 응답 문자열에서 영양 정보를 파싱하는 도우미 함수"""
    nutrients = {
        'calories': r"Calories: (\d+\.?\d*)kcal",
        'fat': r"Fat: (\d+\.?\d*)g",
        'carbohydrate': r"Carbs: (\d+\.?\d*)g",
        'protein': r"Protein: (\d+\.?\d*)g",
    }
    parsed = {}
    for key, pattern in nutrients.items():
        match = re.search(pattern, description)
        if match:
            parsed[key] = float(match.group(1))
    return parsed

def analyze_diet_from_text(food_list):
    """텍스트로 받은 음식 목록의 영양소를 분석하고 조언을 반환하는 함수"""
    total_nutrition = {
        'calories': 0, 'protein': 0, 'carbohydrate': 0, 'fat': 0
    }
    
    try:
        # 1. 각 음식의 영양 정보 조회 및 합산
        for food_item in food_list:
            search_result = fatsecret_api.search_food(food_item)
            if search_result.get('foods') and search_result['foods'].get('food'):
                # 가장 관련성 높은 첫 번째 검색 결과를 사용
                food_data = search_result['foods']['food'][0]
                nutrition_info = parse_nutrition_info(food_data['food_description'])
                for key, value in nutrition_info.items():
                    total_nutrition[key] += value
            else:
                print(f"'{food_item}'에 대한 정보를 찾지 못했습니다.")

        # 2. 일일 권장량과 비교하여 피드백 생성
        feedback = "오늘의 식단 분석 결과입니다.\n"
        feedback += f"- 총 섭취 칼로리: {total_nutrition['calories']:.1f} / {DAILY_RECOMMENDATIONS['calories']} kcal\n"
        feedback += f"- 탄수화물: {total_nutrition['carbohydrate']:.1f} / {DAILY_RECOMMENDATIONS['carbohydrate']} g\n"
        feedback += f"- 단백질: {total_nutrition['protein']:.1f} / {DAILY_RECOMMENDATIONS['protein']} g\n"
        feedback += f"- 지방: {total_nutrition['fat']:.1f} / {DAILY_RECOMMENDATIONS['fat']} g\n\n"

        # 3. 부족한 영양소 기반으로 레시피 추천 (상세 정보 포함)
        if total_nutrition['protein'] < DAILY_RECOMMENDATIONS['protein'] * 0.8:
            feedback += "단백질 섭취가 부족해 보입니다. 단백질 보충을 위해 이런 레시피는 어떠세요?\n"
            recipe_result = fatsecret_api.search_recipe("high protein")
            if recipe_result.get('recipes') and recipe_result['recipes'].get('recipe'):
                recommended_count = 0
                for recipe_summary in recipe_result['recipes']['recipe']:
                    if recommended_count >= 3: # 최대 3개 레시피 추천
                        break
                    try:
                        recipe_details = fatsecret_api.get_recipe_details(recipe_summary['recipe_id'])
                        if recipe_details.get('recipe'):
                            recipe = recipe_details['recipe']
                            # 레시피 설명이 있는 경우에만 추천
                            if recipe.get('recipe_directions') and recipe['recipe_directions'].get('direction'):
                                feedback += f"\n--- 추천 레시피 {recommended_count + 1} ---\n"
                                feedback += f"음식명: {recipe['recipe_name']}\n"

                                # 레시피 영양소 정보 파싱 및 추가
                                if recipe.get('serving_sizes') and recipe['serving_sizes'].get('serving'):
                                    serving = recipe['serving_sizes']['serving']
                                    feedback += f"주요 영양소 (1회 제공량):\n"
                                    feedback += f"  - 칼로리: {serving.get('calories', 'N/A')}kcal\n"
                                    feedback += f"  - 탄수화물: {serving.get('carbohydrate', 'N/A')}g\n"
                                    feedback += f"  - 단백질: {serving.get('protein', 'N/A')}g\n"
                                    feedback += f"  - 지방: {serving.get('fat', 'N/A')}g\n"

                                feedback += f"레시피:\n"
                                if isinstance(recipe['recipe_directions']['direction'], list):
                                    for i, direction in enumerate(recipe['recipe_directions']['direction']):
                                        feedback += f"  {i+1}. {direction['direction_description']}\n"
                                else:
                                    feedback += f"  1. {recipe['recipe_directions']['direction']['direction_description']}\n"
                                
                                feedback += f"필요한 재료:\n"
                                if recipe.get('ingredients') and recipe['ingredients'].get('ingredient'):
                                    if isinstance(recipe['ingredients']['ingredient'], list):
                                        for ingredient in recipe['ingredients']['ingredient']:
                                            feedback += f"  - {ingredient['ingredient_description']}\n"
                                    else:
                                        feedback += f"  - {recipe['ingredients']['ingredient']['ingredient_description']}\n"
                                else:
                                    feedback += "  (재료 정보 없음)\n"
                                recommended_count += 1
                            else:
                                print(f"레시피 '{recipe['recipe_name']}' (ID: {recipe_summary['recipe_id']})는 설명이 없어 추천하지 않습니다.")

                    except Exception as recipe_error:
                        print(f"레시피 상세 정보 가져오기 오류: {recipe_error}")
                        # feedback += f"- {recipe_summary['recipe_name']} (상세 정보 로드 실패)\n"

        return feedback

    except Exception as e:
        print(f"식단 분석 중 오류 발생: {e}")
        return "식단 분석에 실패했습니다. 다시 시도해 주세요."
