
from jamo import h2j, j2hcj
from data import correctAnswer
import re

async def Q4AndQ7Score(text: str):

    q4_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q4"), None)
    if q4_answer is None:

        raise ValueError("Q4 정답을 찾을 수 없습니다.")
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
            
            return 1 if similarity >= 0.6 else 0
        
        @staticmethod
        def calculate_scores(user_words, correct_words):
            """순서 무관하게 단어 매칭하여 점수 계산"""
            scores = []
            used_user_indices = set()  # 이미 매칭된 사용자 단어 인덱스 추적
            
            # 각 정답 단어에 대해
            for correct_word in correct_words:
                max_score = 0
                best_match_index = -1
                
                # 아직 매칭되지 않은 모든 사용자 단어와 비교
                for i, user_word in enumerate(user_words):
                    if i not in used_user_indices:
                        similarity_score = WordSimilarityChecker.calculate_word_similarity(
                            correct_word, user_word
                        )
                        if similarity_score > max_score:
                            max_score = similarity_score
                            best_match_index = i
                
                # 매칭된 단어가 있으면 해당 인덱스를 사용됨으로 표시
                if best_match_index != -1:
                    used_user_indices.add(best_match_index)
                
                scores.append(max_score)
            
            # 정답이 한 단어인 경우 단일 값으로 반환
            if len(correct_words) == 1:
                return scores[0]
            
            return scores

    try:
        checker = WordSimilarityChecker()
        
        # 문자열을 단어 리스트로 변환
        user_words = checker.normalize_text(text)
        correct_words = checker.normalize_text(q4_answer)
        
        # 디버깅용 출력
        print(f"사용자 답변 단어들: {user_words}")
        print(f"정답 단어들: {correct_words}")
        
        # 점수 계산
        result = checker.calculate_scores(user_words, correct_words)
        
        # 디버깅용 출력
        if isinstance(result, list):
            matched_words = []
            scores = []
            for i, score in enumerate(result):
                correct_word = correct_words[i]
                matched_user_word = "없음"
                for j, user_word in enumerate(user_words):
                    if checker.calculate_word_similarity(correct_word, user_word) == 1:
                        matched_user_word = user_word
                        break
                print(f"정답 단어 '{correct_word}' -> 매칭된 단어: '{matched_user_word}', 점수: {score}")
        else:
            print(f"단일 단어: 정답 '{correct_words[0]}' vs 입력 '{user_words[0] if user_words else '없음'}' -> 점수: {result}")
        
        return result

    except Exception as e:
        print(f"Error in Q4AndQ7Score: {str(e)}")
        return 0 if len(checker.normalize_text(q4_answer)) == 1 else [0] * len(checker.normalize_text(q4_answer))