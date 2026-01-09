from nacl.signing import SigningKey
import base64

sk = SigningKey.generate()
pk = sk.verify_key

print("PRIVATE_KEY_BASE64:", base64.b64encode(sk.encode()).decode())
print("PUBLIC_KEY_BASE64 :", base64.b64encode(pk.encode()).decode())
