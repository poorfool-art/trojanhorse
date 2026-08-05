import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ==== НАСТРОЙКИ ====
SOURCE_EXE = r"C:\file\file.exe"     # source file
OUTPUT_FILE = r"C:\crypt\namedat.dat"  # save?
PASSWORD = "88504"                        # pass
SALT = b"static_salt_change_me_1234567890" 
# ====================


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def main():
    key = derive_key(PASSWORD, SALT)
    fernet = Fernet(key)

    with open(SOURCE_EXE, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(encrypted)

    print(f"Готово! Зашифрованный файл сохранён: {OUTPUT_FILE}")
    print("Теперь удали (или перенеси в безопасное место) исходный:")
    print(f"  {SOURCE_EXE}")


if __name__ == "__main__":
    main()
