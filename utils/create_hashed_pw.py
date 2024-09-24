import os
import hashlib
import base64

password = "Password123"

salt = os.urandom(32)
key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
hashed_password = base64.b64encode(salt + key).decode()
print(f"Hashed and salted password: {hashed_password}")