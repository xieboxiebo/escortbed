import base64
import binascii
import re
from Crypto.Cipher import AES


def str_data_2_hex(data):
    sr = "".join([i[2:] for i in data.split(" ")]).encode("utf-8")
    return binascii.a2b_hex(sr)


def add_to_16(text):
    while len(text)%16 !=0:
        text += '\0'
    return text


def AES_Encrypt(key, data):
    str_2_hex = str_data_2_hex(data)
    data = add_to_16(str_2_hex)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypt_data = cipher.encrypt(data)

    bin_data = binascii.b2a_hex(encrypt_data)
    pattern = re.compile('.{2}')
    # findall是找到所有的字符,再在字符中添加空格，当然你想添加其他东西当然也可以
    encrypt = "0x" + ' 0x'.join(pattern.findall(bin_data.decode("utf-8")))
    return encrypt

def AES_Decrypt(key, data):
    str_2_hex = str_data_2_hex(data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypt_data = cipher.decrypt(str_2_hex)
    bin_data = binascii.b2a_hex(decrypt_data)
    pattern = re.compile('.{2}')
    # findall是找到所有的字符,再在字符中添加空格，当然你想添加其他东西当然也可以
    decrypt = "0x" + ' 0x'.join(pattern.findall(bin_data.decode("utf-8")))
    return decrypt

if __name__ == '__main__':
    key = b"\x3A\x60\x43\x2A\x5C\x01\x21\x1F\x29\x1E\x0F\x4E\x0C\x13\x28\x25"
    # data1 = b"\x06\x01\x01\x01\x2C\x2C\x62\x58\x26\x67\x42\x66\x01\x33\x31\x41"
    data1 = b'\x06\x01\x01\x01,,bX&gBf\x0131A'
    b'\xBA\x13\x9E\xF9\xC0\xE4\x80\xA5\xAB\xD4\xE2\xAB\xD3\xDB\x91\x47'
    da = "0x06 0x01 0x01 0x01 0x2C 0x2C 0x62 0x58 0x26 0x67 0x42 0x66 0x01 0x33 0x31 0x41"

    da2 = '0xBA 0x13 0x9E 0xF9 0xC0 0xE4 0x80 0xA5 0xAB 0xD4 0xE2 0xAB 0xD3 0xDB 0x91 0x47'
    print("加密", AES_Encrypt(key, "0x05 0x01 0x06 0x30 0x30 0x30 0x30 0x30 0x30 0x08 0x66 0x84 0x23 0x5E 0x26 0x36"))
    print("解密", AES_Decrypt(key, "0x1F 0xBE 0x9E 0x1C 0x27 0x45 0x4E 0x9D 0xEB 0x4D 0xA8 0x79 0xF0 0xB3 0xE5 0x09"))


