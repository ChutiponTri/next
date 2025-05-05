import random
import string

def generate_token(length=12):
    random.seed(16102001)
    all_chars = string.ascii_letters + string.digits + string.punctuation
    token = ''.join(random.choices(all_chars, k=length))
    return token

def generate_x_token():
    random.seed(16102001)
    word1 = ''.join(random.choices(string.ascii_lowercase, k=4))  # 4-letter word
    word2 = ''.join(random.choices(string.ascii_lowercase, k=6))  # 6-letter word
    word3 = ''.join(random.choices(string.ascii_lowercase, k=5))  # 5-letter word

    # Combine them with hyphens to create the token
    x_token = f"{word1}-{word2}-{word3}"
    return x_token
