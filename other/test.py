# coding=utf-8
import constants
from pro_vestvirus.encrypt.AesEncry import AESCipher
from plugin.FilePlugin import *


# os.chdir("/Users/sung/sung/flutter-project/huajian-android")
# os.system("./gradle clean assembleRelease")

# with subprocess.Popen(["./gradlew", "assembleRelease"], shell=False,
#                       cwd="/Users/sung/sung/flutter-project/huajian-android") as p:
#     print(">>>>>>>>>>>>" + str(p.wait()))


# FilePlugin.remove_path(constants.path_self + "/aaaaa/aaab/asdca")

# for file in FileFinder.find_file_in_dir(os.path.join(constants.path_self, 'pro_yrjiagu'), '.py'):
#     print(str(file))

# Reediter.reedit_hook_application_aes_ini(constants.aes_key,constants.aes_iv)

# name = "zhou"
# name2 = "zhou1"
# 多个%s在替换的时候需要后者以元组形式入参
# print("%s%s" % (name, name2))
# print("%s%d" % ("zhou", 111))

# join方法前者会插分式的插入后者的每一个字符中间
# print("hello".join("world"))
# print(" ".join(("hello", "world", "!")))

# 有色内容打印
# print("\033[4;36;42m输出内容\033[0m")
# 7反白状态下字体色会变成背景色
# print("\033[2;31m输出内容\033[0m")
# print(("执行方法%s耗时 >>> %d ms" % (str("aaaaaa"), 4444)).join(("\033[7m", "\033[0m")))

# text = """
# public interface OnAnimListener
#     {
#         void onAnimStart();
#
#         void onAnimFinish();
#     }
# """
# f = text.replace("OnAnimListener\n", "OnAnimListener")
# print(f'{f}')


# from plugin.DictPlugin import *
# print(f'{DictPlugin.random_string_full(16)}')


# from pro_vestvirus.encrypt.AesEncry import *
#
# domain = 'YapKaL1F5z5itlUYJJ7dGQ=='
# aes = AESCipher('KluXvp7UC0VnePtH')
# print(aes.encrypt('aaaaaaaaaaaaa'))
# print(aes.decrypt(domain))

# from pro_assembleapk.Git import *
# git = Git(os.path.join(constants.path_root, "flutter-project/huajian-android"))
# git.reset_last_()


def encrypt_string(key, string):
    aes = AESCipher(key)
    strings = aes.encrypt(string)
    print(f'加密前 --> {string} 加密后 --> {strings}')
    return strings


def decrypt_string(key, string):
    aes = AESCipher(key)
    strings = aes.decrypt(string)
    print(f'解密前 --> {string} 解密后 --> {strings}')
    return strings

# encrypt_string('KluXvp7UC0VnePtH', 'VTHUAJIAN')
# encrypt_string('KluXvp7UC0VnePtH', '1')


FilePlugin.change_str_in_binaryfile("aaa花花","huajian",os.path.join(constants.path_self,"resources.arsc"))
