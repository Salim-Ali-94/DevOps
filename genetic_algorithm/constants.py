import string


NUMBERS = [str(number) for number in range(10)]
ALPHABETS = list(string.ascii_lowercase) + list(string.ascii_uppercase)
SYMBOLS = list(string.punctuation) + ["_", "\\", "%", "*", "^", ]
CHARACTERS = ALPHABETS + NUMBERS + SYMBOLS
