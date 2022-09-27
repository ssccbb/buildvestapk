import base64
import os, constants
from random import Random

from Cryptodome.Cipher import AES


class AESPlugin:
    key = ''
    iv = ''

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt_str(self, data, password):
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        iv = Random.new().read(bs)
        cipher = AES.new(password, AES.MODE_CBC, iv)
        data = cipher.encrypt(pad(data))
        data = iv + data
        return (data)

    def decrypt_str(self, data, password):
        bs = AES.block_size
        if len(data) <= bs:
            return (data)
        unpad = lambda s: s[0:-ord(s[-1])]
        iv = data[:bs]
        cipher = AES.new(password, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(data[bs:]))
        return (data)

    def encrypt_str_base64(self, data):
        aes = AES.new(key=self.add_to_16(self.key), mode=AES.MODE_CBC, iv=self.iv.encode())
        encryptedstr = aes.encrypt(self.add_to_16(data))  # 加密后得到的字节数据
        en_str = base64.b64encode(encryptedstr)  # 以base64编码方式解码, 得到加密字符串!
        return str(en_str,encoding='utf-8')  # 把加密后的字节数据返回

    def decrypt_str_base64(self, data):
        # 解密时必须重新构建aes对象
        aes = AES.new(key=self.add_to_16(self.key), mode=AES.MODE_CBC, iv=self.iv.encode())
        # 先把密文转换成字节型, 再解密, 最后把之前填充的'\x00' 去掉
        decryptedstr = aes.decrypt(base64.decodebytes(data.encode()))
        return str(decryptedstr, encoding='utf-8').strip('\x00')


    # 待加密文本补齐到 block size 的整数倍
    def padding(self, bytes):
        while len(bytes) % AES.block_size != 0:  # 循环直到补齐 AES_BLOCK_SIZE 的倍数
            bytes += ' '.encode()  # 通过补空格（不影响源文件的可读）来补齐
        return bytes  # 返回补齐后的字节列表

    # 待加密文本补齐到 block size 的整数倍
    def un_padding(self, bytes):
        while len(bytes) % AES.block_size != 0:  # 循环直到补齐 AES_BLOCK_SIZE 的倍数
            bytes -= ' '.encode()  # 通过补空格（不影响源文件的可读）来补齐
        return bytes  # 返回补齐后的字节列表

    # 加密函数
    def encrypt_byte(self, bytes):
        # 填充数据
        bytes = self.padding(bytes)
        cryptor = AES.new(str.encode(self.key), AES.MODE_CBC, str.encode(self.iv))
        ciphertext = cryptor.encrypt(bytes)
        return ciphertext

    # 解密函数
    def decrypt_byte(self, bytes):
        cryptor = AES.new(str.encode(self.key), AES.MODE_CBC, str.encode(self.iv))
        cipherbyte = cryptor.decrypt(bytes)
        # 去除填充数据
        cipherbyte = self.un_padding(cipherbyte)
        return cipherbyte

    # 加密文件
    def encrypt_byte_by_jar(self, file, encrypt_file):
        path_endecrypt = os.path.join(constants.path_self, "jar/encrypt_tool.jar")
        cmd = f'java -jar {path_endecrypt} {file} {encrypt_file} {self.key} {self.iv} encrypt'
        if os.system(cmd) == 0:
            print("文件加密成功")
        else:
            print("文件加密失败")

    # 解密文件
    def decrypt_byte_by_java(self, file, encrypt_file):
        path_endecrypt = os.path.join(constants.path_self, "jar/encrypt_tool.jar")
        cmd = f'java -jar {path_endecrypt} {file} {encrypt_file} {self.key} {self.iv} decrypt'
        if os.system(cmd) == 0:
            print("文件解密成功")
        else:
            raise Exception("文件解密失败")

    def add_to_16(self, value):
        while len(value.encode('utf-8')) % 16 != 0:
            value += '\x00'  # 补全, 明文和key都必须是16的倍数
        return value.encode('utf-8')
