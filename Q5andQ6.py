async def Q5AndQ6Score(text: str, correctAnswer: str):
    
    class NumberSimilarityChecker:
        # 숫자별 한글 발음 매핑 (한글로 말한 경우도 처리)
        NUMBER_MAPPING = {
            '0': ['0', '영', '공'],
            '1': ['1', '일'],
            '2': ['2', '이'],
            '3': ['3', '삼'],
            '4': ['4', '사'],
            '5': ['5', '오'],
            '6': ['6', '육', '엿'],
            '7': ['7', '칠'],
            '8': ['8', '팔'],
            '9': ['9', '구'],
        }
        
        @staticmethod
        def normalize_number(text):
            """숫자나 한글을 정규화된 숫자 형태로 변환"""
            normalized = ''
            text = text.replace(" ", "")  # 공백 제거
            
            # 한글 또는 숫자를 정규화된 숫자로 변환
            for char in text:
                for num, variations in NumberSimilarityChecker.NUMBER_MAPPING.items():
                    if char in variations:
                        normalized += num
                        break
            
            return normalized
        
        @staticmethod
        def calculate_similarity(text1, text2):
            """두 텍스트의 유사도를 계산"""
            # 정규화
            norm1 = NumberSimilarityChecker.normalize_number(text1)
            norm2 = NumberSimilarityChecker.normalize_number(text2)
            
            # 디버깅을 위한 출력
            print(f"Original - Text: {text1}, Example: {text2}")
            print(f"Normalized - Text: {norm1}, Example: {norm2}")
            
            if not norm1 or not norm2:  # 둘 중 하나라도 숫자로 변환되지 않은 경우
                return 0.0
                
            if norm1 == norm2:  # 완전 일치
                return 1.0
                
            # 순서가 뒤바뀐 경우나 부분 일치는 모두 0 반환
            return 0.0

    try:
        # 점수 계산
        checker = NumberSimilarityChecker()
        similarity_score = checker.calculate_similarity(text, correctAnswer)
        
        # 완전 일치(100%)인 경우 1, 그 외에는 0 반환
        final_score = 1 if similarity_score == 1.0 else 0
        
        # 디버깅 정보 출력
        print(f"Similarity score: {similarity_score * 100:.1f}%")
        print(f"Final score: {final_score}")
        
        return final_score
        
    except Exception as e:
        print(f"Error in Q5_score: {str(e)}")
        return 0