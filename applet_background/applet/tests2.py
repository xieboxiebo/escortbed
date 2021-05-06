# import base64
# import binascii
# import re
# from Crypto.Cipher import AES
#
#
# class AESCBC:
#     def __init__(self):
#         # self.key = 'msunsoftalphaicd'.encode('utf-8')  # 定义key值
#         self.key = 'msunsoftalphaicd'.encode('utf-8')  # 定义key值
#         self.mode = AES.MODE_CBC
#         self.bs = 16  # block size
#         self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
#
#     # 加密
#     def encrypt(self, text):
#         generator = AES.new(self.key, self.mode, self.key)  # 这里的key 和IV 一样 ，可以按照自己的值定义
#         crypt = generator.encrypt(self.PADDING(text).encode('utf-8'))
#         crypted_str = base64.b64encode(crypt)  # 输出Base64
#         # crypted_str = binascii.b2a_hex(crypt)  # 输出Hex
#         result = crypted_str.decode()
#         return result
#
#     # 解密
#     def decrypt(self, text):
#         generator = AES.new(self.key, self.mode, self.key)
#         text += (len(text) % 4) * '='
#         decrpyt_bytes = base64.b64decode(text)  # 输出Base64
#         # decrpyt_bytes = binascii.a2b_hex(text)  # 输出Hex
#         meg = generator.decrypt(decrpyt_bytes)
#         # 去除解码后的非法字符
#         try:
#             result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
#         except Exception:
#             result = '解码失败，请重试!'
#         return result


import base64
import hashlib
from Crypto.Cipher import AES as _AES


class AES:

    def __init__(self, key: str):
        """Init aes object used by encrypt or decrypt.
        AES/ECB/PKCS5Padding  same as aes in java default.
        """

        self.aes = _AES.new(self.get_sha1prng_key(key), _AES.MODE_ECB)

    @staticmethod
    def get_sha1prng_key(key: str) -> bytes:
        """encrypt key with SHA1PRNG.
        same as java AES crypto key generator SHA1PRNG.
        SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG" );
        secureRandom.setSeed(decryptKey.getBytes());
        keygen.init(128, secureRandom);
        :param string key: original key.
        :return bytes: encrypt key with SHA1PRNG, 128 bits or 16 long bytes.
        """

        signature: bytes = hashlib.sha1(key.encode()).digest()
        signature: bytes = hashlib.sha1(signature).digest()
        return signature[:16]

    @staticmethod
    def padding(s: str) -> str:
        """Padding PKCS5"""

        pad_num: int = 16 - len(s) % 16
        return s + pad_num * chr(pad_num)

    @staticmethod
    def unpadding(s):
        """Unpadding PKCS5"""

        padding_num: int = ord(s[-1])
        return s[: -padding_num]

    def encrypt_to_bytes(self, content_str):
        """From string encrypt to bytes ciphertext.
        """

        content_bytes = self.padding(content_str).encode()
        ciphertext_bytes = self.aes.encrypt(content_bytes)
        return ciphertext_bytes

    def encrypt_to_base64(self, content_str):
        """From string encrypt to base64 ciphertext.
        """

        ciphertext_bytes = self.encrypt_to_bytes(content_str)
        ciphertext_bs64 = base64.b64encode(ciphertext_bytes).decode()
        return ciphertext_bs64

    def decrypt_from_bytes(self, ciphertext_bytes):
        """From bytes ciphertext decrypt to string.
        """

        content_bytes = self.aes.decrypt(ciphertext_bytes)
        content_str = self.unpadding(content_bytes.decode())
        return content_str

    def decrypt_from_base64(self, ciphertext_bs64):
        """From base64 ciphertext decrypt to string.
        """

        ciphertext_bytes = base64.b64decode(ciphertext_bs64)
        content_str = self.decrypt_from_bytes(ciphertext_bytes)
        return content_str


def encrypt_to_bytes(content_str, encrypt_key: str):
    """From string encrypt to bytes ciphertext.
    """

    aes: AES = AES(encrypt_key)
    ciphertext_bytes = aes.encrypt_to_bytes(content_str)
    return ciphertext_bytes


def encrypt_to_base64(content_str, encrypt_key: str) -> str:
    """From string encrypt to base64 ciphertext.
    """

    aes: AES = AES(encrypt_key)
    ciphertext_bs64 = aes.encrypt_to_base64(content_str)
    return ciphertext_bs64


def decrypt_from_bytes(ciphertext_bytes, decrypt_key: str) -> str:
    """From bytes ciphertext decrypt to string.
    """

    aes: AES = AES(decrypt_key)
    content_str = aes.decrypt_from_bytes(ciphertext_bytes)
    return content_str


def decrypt_from_base64(ciphertext_bs64, decrypt_key: str) -> str:
    """From base64 ciphertext decrypt to string.
    """

    aes: AES = AES(decrypt_key)
    content_str = aes.decrypt_from_base64(ciphertext_bs64)
    return content_str


if __name__ == "__main__":
    key = "57bf1661-3aad-4786-89a2-e187b38966ea"
    ct = "uafBlgURdmIJtSSe5Li/V1mByS3XZrpjXL+F/FCJmmro1bczVkVuHBBGcIk+Msi6hRSdCyJGZ+ox\nRHEA/QL0WjNXqw0BhgXE6oWYe/d0o3w="
    ret = decrypt_from_base64(ct, key)
    print(ret)

# if __name__ == '__main__':
#     a = AESCBC()
#     print(a.encrypt('123456'))
#     print(a.decrypt(a.encrypt('123456')))

    key = bytearray([0x3A, 0x60, 0x43, 0x2A, 0x5C, 0x01, 0x21, 0x1F, 0x29, 0x1E, 0x0F, 0x4E, 0x0C, 0x13, 0x28, 0x25])
    # key = bytearray([0x3A, 0x60, 0x43, 0x2A, 0x5C, 0x01, 0x21, 0x1F, 0x29, 0x1E, 0x0F, 0x4E, 0x0C, 0x13, 0x28, 0x25])

    data = bytearray([0x06, 0x01, 0x01, 0x01, 0x2C, 0x2C, 0x62, 0x58, 0x26, 0x67, 0x42, 0x66, 0x01, 0x33, 0x31, 0x41])
    en_data = encrypt_to_base64(data, key)
    print(en_data, 8888)