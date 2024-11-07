from jamo import h2j, j2hcj
import re
from typing import List, Dict
from statistics import mean, stdev

class FormSimilarityAnalyzer:
    def __init__(self):
        # 테스트할 변형 단어들과 각각이 맞는지 틀린지 여부
        self.test_variations = {
            "시계": [
                ("시계", True),  # 정확한 발음
                ("시게", True),  # ㅖ 발음이 ㅔ로 인식
                ("식계", True),  # ㅣ와 ㅏ의 혼동
                ("시걔", True),  # ㄱ과 ㄲ의 발음 혼동
                ("시겨", True),  # ㅖ가 ㅕ로 인식되는 경우
                ("시게이", True),  # 끝에 이가 붙는 경우
                ("씨계", True),  # ㅅ이 강하게 들린 경우
                ("시기", True),  # ㅖ가 ㅣ로 인식되는 경우
                ("시카", True),  # ㅔ가 ㅏ로 인식되는 경우
                ("시켸", True),  # ㅖ와 ㅔ의 혼동
                ("ㅅ계", True),  # 첫 소리의 약음화
                ("지계", True),  # ㅅ과 ㅈ의 혼동
                ("쉬계", True),  # ㅣ와 ㅟ의 혼동
                ("쉬게", True),  # ㅟ와 ㅔ의 혼동
                ("시켸", True),  # 발음의 혼동
                ("씨게", True),  # ㅅ의 중복
                ("시께", True),  # ㄱ과 ㄲ의 혼동
                ("시꺠", True),  # ㄲ과 ㄱ의 혼동
                ("식계", True),  # ㅣ가 강하게 들리는 경우
                ("시개", False),  # 발음이 완전히 달라 정답으로 보기 어려움
                ("기계", False),  # 다른 의미의 단어
                ("시계아", False),  # 의미가 달라 정답으로 보기 어려움
                ("시기아", False),  # 무의미한 변형
                ("시계야", False),  # 끝에 '야'가 붙은 경우
            ]
        }

    def decompose_hangul(self, word: str) -> List[str]:
        """한글 단어를 자모 단위로 분해"""
        try:
            return list(j2hcj(h2j(word)))
        except:
            return list(word)

    def calculate_similarity(self, word1: str, word2: str) -> float:
        """두 단어 간의 자모 유사도 계산"""
        jamo1 = self.decompose_hangul(word1)
        jamo2 = self.decompose_hangul(word2)
        
        length_diff = abs(len(jamo1) - len(jamo2))
        length_penalty = max(0, 1 - (length_diff * 0.1))
        
        max_len = max(len(jamo1), len(jamo2))
        min_len = min(len(jamo1), len(jamo2))
        
        matches = sum(1 for i in range(min_len) if jamo1[i] == jamo2[i])
        base_similarity = matches / max_len
        
        final_similarity = base_similarity * length_penalty
        return round(final_similarity, 3)

    def analyze_variations(self, target_word: str) -> Dict:
        """단어의 다양한 변형에 대한 유사도 분석"""
        variations = self.test_variations.get(target_word, [])
        if not variations:
            return None
        
        correct_scores = []
        incorrect_scores = []
        
        print(f"\n'{target_word}'에 대한 형태적 유사도 분석:")
        print("-" * 35)
        print(f"{'변형단어':<10} {'유사도':>8} {'정답여부':>8}")
        print("-" * 35)
        
        for var, is_correct in variations:
            similarity = self.calculate_similarity(target_word, var)
            print(f"{var:<10} {similarity:>8.3f} {'O' if is_correct else 'X':>8}")
            
            if is_correct:
                correct_scores.append(similarity)
            else:
                incorrect_scores.append(similarity)

        print("\n통계 분석:")
        print(f"정답으로 처리된 변형들의 평균 유사도: {mean(correct_scores):.3f}")
        print(f"오답으로 처리된 변형들의 평균 유사도: {mean(incorrect_scores):.3f}")
        print(f"정답 변형들의 최소 유사도: {min(correct_scores):.3f}")
        print(f"오답 변형들의 최대 유사도: {max(incorrect_scores):.3f}")
        
        # 추천 임계값: 정답 최소값과 오답 최대값의 중간값
        recommended_threshold = (min(correct_scores) + max(incorrect_scores)) / 2
        print(f"추천 임계값: {recommended_threshold:.3f}")

# 테스트
if __name__ == "__main__":
    analyzer = FormSimilarityAnalyzer()
    analyzer.analyze_variations("시계")