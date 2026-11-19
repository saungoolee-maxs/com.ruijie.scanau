import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

SALT = "tinseinandha9vipgyi"     # BL ေတွလားဟ ?
NEW_EXPIRY_MS = 1999999999999    # 2033-05-18 (Extending your key)



key = hashlib.sha256(SALT.encode()).digest()
print(f"[1] Derived Key: {key.hex()}")


new_ts_bytes = str(NEW_EXPIRY_MS).encode()
print(f"[2] Plaintext: '{NEW_EXPIRY_MS}'")


padder = padding.PKCS7(128).padder() 
padded_ts = padder.update(new_ts_bytes) + padder.finalize()
print(f"[3] Padded Hex: {padded_ts.hex()}")


cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()
new_ct = encryptor.update(padded_ts) + encryptor.finalize()


new_key = base64.b64encode(new_ct).decode()
print(f"\n[+] NEW KEY: {new_key}")


decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(new_ct) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
decrypted_ts = unpadder.update(decrypted_padded) + unpadder.finalize()
print(f"[+] Verification (Decrypted): '{decrypted_ts.decode()}'")
