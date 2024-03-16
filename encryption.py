from cryptography.fernet import Fernet

with open('key.txt', 'rb') as f:
    key = f.read()
f = Fernet(key)

def encrypt(text:str) -> str:
    token = f.encrypt(str.encode(text)) #encrypted text in bytes
    return token.decode("utf-8") #returns encrypted text in string

def decrypt(token:str) -> str:
    return f.decrypt(token).decode("utf-8")