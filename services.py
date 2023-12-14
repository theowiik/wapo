import random
from english_words import get_english_words_set


def get_solution(word_length: int) -> str:
    """
    Get the solution of a word "based on" a hint and word length.
    """
    try:
        word_length = int(word_length)
    except:
        return 'Please provide a number for the word length ✋😒'

    if word_length <= 0:
        return 'Please provide a positive number ☝️😫'

    word_set = get_english_words_set(['gcide'], lower=True)
    words_correct_length = [
        word for word in word_set if len(word) == word_length]

    if not words_correct_length:
        return 'No words found with that length 😢'

    return f'✅ The word is: "{random.choice(words_correct_length)}" ☝️🤓 ✅'
