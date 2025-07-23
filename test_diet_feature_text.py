
# test_diet_feature_text.py
import os
import sys

# src 폴더를 sys.path에 추가하여 모듈을 찾을 수 있도록 함
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from features.diet import diet

def run_test():
    """텍스트 기반 식단 분석 기능 테스트 실행 함수"""
    print("테스트 시작: 텍스트로 입력된 음식 목록을 분석합니다...")
    
    # 테스트할 음식 목록
    my_lunch = ["hamburger", "coca-cola", "ice cream"]
    
    try:    
        # 식단 분석 함수 호출
        result_message = diet.analyze_diet_from_text(my_lunch)

        # 결과 출력
        print('\n--- 최종 분석 결과 ---')
        print(result_message)

    except Exception as e:
        print(f'\n--- 테스트 실패 ---')
        print(e)

if __name__ == "__main__":
    run_test()

