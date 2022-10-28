import os
import re

from plugin.DictPlugin import DictPlugin
from plugin.FilePlugin import *
from pro_vestvirus.encrypt.AesEncry import *

class AES:

    def __init__(self, path_android):
        self.params_regular = f'public\\s+static\\s+final\\s+String\\s+([\\w_]+)\\s+=\\s+VestHelper\\.getInstance\\(\\)\\.decodeAESString\\(".*"\\);?'

        # yrAppKey yrAppId nimKey umengKey
        self.path_gradle = os.path.join(path_android, 'config.gradle')
        # KEY_OPENINSTALL MAIN_CHANNEL SUB_CHANNEL
        self.path_properties = os.path.join(path_android, 'gradle.properties')
        # aesDecoder\\("\\w+"\\)
        self.path_app_gradle = os.path.join(path_android, 'app/build.gradle')
        self.path_target_file = os.path.join(path_android, 'library-commonlib/src/main/java/com/yr/common/vest/VestHelper.java')
        self.path_files = [os.path.join(path_android, 'app/src/main/assets/domain_data.txt'),
                           os.path.join(path_android, 'app/src/main/assets/domain_evn_data.txt'),
                           os.path.join(path_android, 'app/src/main/assets/hj_privacy_enquire.txt')]

        self.old_aes_key = self.read_old_aes_key()
        self.new_aes_key = DictPlugin.random_string_full(16)
        pass

    def read_old_aes_key(self):
        config_content = FilePlugin.read_str_from_file(self.path_gradle)
        result = re.compile(f'aeskey\\s+:\\s+\"\\w+\"').search(config_content)
        if result is None:
            return None
        result = result.group().lstrip().strip().replace(' ', '')
        return result[result.rindex(':') + 1:len(result)].replace('"', '').replace('\'', '')

    def encrypt_string(self, decrypt_string):
        aes = AESCipher(self.new_aes_key)
        strings = aes.encrypt(decrypt_string)
        print(f'加密前 --> {decrypt_string} 加密后 --> {strings}')
        return strings

    def decrypt_string(self, encrypt_string):
        aes = AESCipher(self.old_aes_key)
        strings = aes.decrypt(encrypt_string)
        print(f'解密前 --> {encrypt_string} 解密后 --> {strings}')
        return strings

    def get_new_encrypt_string(self, encrypt_string):
        decrypt_string = self.decrypt_string(encrypt_string)
        if decrypt_string is None:
            print(f'使用 {self.old_aes_key} 解密 {encrypt_string} 失败!')
            return None
        return self.encrypt_string(decrypt_string)
