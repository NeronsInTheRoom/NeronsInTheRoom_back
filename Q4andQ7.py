from jamo import h2j, j2hcj
import re

async def Q4AndQ7Score(text: str, correctAnswer: str):
    class WordSimilarityChecker:
        @staticmethod
        def normalize_text(text):
            """쉼표나 공백으로 구분된 문자열을 단어 리스트로 변환"""
            words = re.split('[,\s]+', text.strip())
            return [word.strip() for word in words if word.strip()]

        @staticmethod
        def decompose_hangul(word):
            """한글 단어를 자모 단위로 분해"""
            return list(j2hcj(h2j(word)))

        @staticmethod
        def calculate_word_similarity(word1, word2):
            """두 단어 간의 자모 유사도 계산"""
            jamo1 = WordSimilarityChecker.decompose_hangul(word1)
            jamo2 = WordSimilarityChecker.decompose_hangul(word2)
            
            max_len = max(len(jamo1), len(jamo2))
            min_len = min(len(jamo1), len(jamo2))
            
            matches = sum(1 for i in range(min_len) if jamo1[i] == jamo2[i])
            similarity = matches / max_len
            
            return 1 if similarity >= 0.8 else 0

        @staticmethod
        def calculate_ordered_scores(user_words, correct_words):
            """순서를 고려하여 점수 계산"""
            scores = [0] * len(correct_words)  # 모든 점수를 0으로 초기화
            
            # 각 위치별로 점수 계산
            for i, correct_word in enumerate(correct_words):
                if i < len(user_words):  # 사용자가 해당 위치에 단어를 입력했는지 확인
                    similarity_score = WordSimilarityChecker.calculate_word_similarity(
                        correct_word, user_words[i]
                    )
                    scores[i] = similarity_score
            
            return scores

    try:
        checker = WordSimilarityChecker()
        
        # 문자열을 단어 리스트로 변환
        user_words = checker.normalize_text(text)
        correct_words = checker.normalize_text(correctAnswer)
        
        # 디버깅용 출력
        print(f"사용자 답변 단어들: {user_words}")
        print(f"정답 단어들: {correct_words}")
        
        # 순서를 고려한 점수 계산
        scores = checker.calculate_ordered_scores(user_words, correct_words)
        
        # 디버깅용 출력
        for i, (word, score) in enumerate(zip(correct_words, scores)):
            print(f"{i+1}번째 단어: 정답 '{word}' vs 입력 '{user_words[i] if i < len(user_words) else '없음'}' -> 점수: {score}")
        
        return scores

    except Exception as e:
        print(f"Error in Q4_score: {str(e)}")
        return [0, 0, 0]
