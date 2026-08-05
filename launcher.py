import os
import sys
import time
import base64
import getpass
import tempfile
import subprocess

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ==== НАСТРОЙКИ (должны совпадать с encrypt_program.py) ====
ENCRYPTED_FILE = r"C:\Windows\Microsoft\sys_cache_4471.dat" #save
SALT = b"static_salt_change_me_1234567890"
DECOY_PROGRAM_PATH = r"D:\Programs\Sublime Text\sublime_text.exe" #random program u pc
MAX_ATTEMPTS = 3
# =============================================================


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def try_decrypt(password: str):
    key = derive_key(password, SALT)
    fernet = Fernet(key)
    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted = f.read()
    try:
        return fernet.decrypt(encrypted)
    except InvalidToken:
        return None


def run_decrypted(data: bytes):
    # Создаём временный exe со случайным именем, запускаем, потом чистим
    tmp_dir = tempfile.mkdtemp(prefix="~tmp")
    tmp_exe = os.path.join(tmp_dir, "cdn_updater.exe")
    with open(tmp_exe, "wb") as f:
        f.write(data)

    proc = subprocess.Popen([tmp_exe])
    proc.wait()  # ждём закрытия программы

    try:
        os.remove(tmp_exe)
        os.rmdir(tmp_dir)
    except OSError:
        pass


def main():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        password = getpass.getpass("Введите пароль: ")
        data = try_decrypt(password)
        if data is not None:
            run_decrypted(data)
            return
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"Неверный пароль. Осталось попыток: {remaining}")

    subprocess.Popen([DECOY_PROGRAM_PATH])


if __name__ == "__main__":
    main()
