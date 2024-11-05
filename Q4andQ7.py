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
        def calculate_scores(user_words, correct_words):
            """단어 개수에 따라 유동적으로 점수 계산"""
            scores = []
            
            # 각 위치별로 점수 계산
            for i, correct_word in enumerate(correct_words):
                if i < len(user_words):  # 사용자가 해당 위치에 단어를 입력했는지 확인
                    similarity_score = WordSimilarityChecker.calculate_word_similarity(
                        correct_word, user_words[i]
                    )
                    scores.append(similarity_score)
            
            # 입력되지 않은 나머지 정답 단어들에 대해 0점 처리
            scores.extend([0] * (len(correct_words) - len(scores)))
            
            # 정답이 한 단어인 경우 단일 값으로 반환
            if len(correct_words) == 1:
                return scores[0]
            
            return scores

    try:
        checker = WordSimilarityChecker()
        
        # 문자열을 단어 리스트로 변환
        user_words = checker.normalize_text(text)
        correct_words = checker.normalize_text(correctAnswer)
        
        # 디버깅용 출력
        print(f"사용자 답변 단어들: {user_words}")
        print(f"정답 단어들: {correct_words}")
        
        # 점수 계산
        result = checker.calculate_scores(user_words, correct_words)
        
        # 디버깅용 출력
        if isinstance(result, list):
            for i, (word, score) in enumerate(zip(correct_words, result)):
                print(f"{i+1}번째 단어: 정답 '{word}' vs 입력 '{user_words[i] if i < len(user_words) else '없음'}' -> 점수: {score}")
        else:
            print(f"단일 단어: 정답 '{correct_words[0]}' vs 입력 '{user_words[0] if user_words else '없음'}' -> 점수: {result}")
        
        return result

    except Exception as e:
        print(f"Error in Q4AndQ7Score: {str(e)}")
        # 에러 발생 시 정답 단어 개수에 따라 반환값 형식 결정
        return 0 if len(checker.normalize_text(correctAnswer)) == 1 else [0] * len(checker.normalize_text(correctAnswer))