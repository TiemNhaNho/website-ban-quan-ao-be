import string
import random

LOWERCASE = list(string.ascii_lowercase)
UPPERCASE = list(string.ascii_uppercase)
DIGITS = list(string.digits)
PUNCTUATION = list(string.punctuation)

# DEFAULT_PASSWORD_LENGTH = 10

def generate_password() -> str:
    random.shuffle(LOWERCASE)  
    random.shuffle(UPPERCASE)  
    random.shuffle(DIGITS)  
    random.shuffle(PUNCTUATION)  
    
    password = []
    password.extend(LOWERCASE[:3])  
    password.extend(UPPERCASE[:3])  
    password.extend(DIGITS[:2])  
    password.extend(PUNCTUATION[:2])
    
    random.shuffle(password)
    
    return ''.join(password)