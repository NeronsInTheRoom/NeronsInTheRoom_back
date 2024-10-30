async def Q5_score(text: str, example: str):
    
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
                
            # 부분 점수 계산
            score = 0.0
            min_len = min(len(norm1), len(norm2))
            
            # 각 자리수별로 비교
            for i in range(min_len):
                if norm1[i] == norm2[i]:
                    score += 1.0
            
            # 전체 자리수로 나누어 정규화
            max_len = max(len(norm1), len(norm2))
            final_score = score / max_len
            
            # 순서가 뒤바뀐 경우 추가 체크
            if final_score == 0 and len(norm1) == len(norm2) == 2:
                if norm1[0] == norm2[1] and norm1[1] == norm2[0]:
                    final_score = 0.5  # 순서가 바뀐 경우 50% 점수
            
            return final_score

    try:
        # 점수 계산
        checker = NumberSimilarityChecker()
        score = checker.calculate_similarity(text, example)
        
        # 디버깅 정보 출력
        print(f"Final score: {score * 100:.1f}%")
        
        return score
        
    except Exception as e:
        print(f"Error in Q5_score: {str(e)}")
        return 0.0
