import re

def find_shift(known_word: str, word_in_original: str) -> int:
    shift = (ord(known_word[0]) - ord(word_in_original[0])) % 26
    for i in range(1, len(known_word)):
        if (ord(known_word[i]) - ord(word_in_original[i])) % 26 != shift:
            return None
    return shift

def apply_shift(sentence: str, shift: int) -> str:
    shifted_sentence = []
    for char in sentence:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shifted_char = chr(((ord(char) - base + shift) % 26) + base)
            shifted_sentence.append(shifted_char)
        else:
            shifted_sentence.append(char)
    return ''.join(shifted_sentence)

def clean_sentence(sentence: str) -> str:
    return re.sub(r'[^a-zA-Z]', '', sentence)

def deciphered_sentence(original_sentence: str, known_word: str) -> str:
    words = re.findall(r'[a-zA-Z]+', original_sentence)
    for word in words:
        if len(word) == len(known_word):
            shift = find_shift(known_word, clean_sentence(word))
            if shift is not None:
                return apply_shift(original_sentence, shift)
    return "invalid"


original_sentence = "Coding was super fun!"
known_word = "gvo"
expected_output = "Dpejoh xbt tvqfs gvo!"
result = deciphered_sentence(original_sentence, known_word)
try:
    assert result == expected_output
    print(f"Test passed!\nExpected: '{expected_output}'\nProduced: '{result}'")
except AssertionError:
    print(f"Test failed!\nExpected: '{expected_output}'\nProduced: '{result}'")
