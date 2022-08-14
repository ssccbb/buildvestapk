import os
import re
import sys
import time

import constants
from plugin.APKPlugin import APKPlugin
from plugin.FilePlugin import FilePlugin
from plugin.SearchPlugin import FileFinder


def deco(func):
    """
    装饰器打印方法耗时
    :param func: 执行的方法
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(("开始执行 >>> %s" % str(func)).join(("\033[7m", "\033[0m")))
        func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print(("执行方法%s耗时 >>> %d ms" % (str(func), msecs)).join(("\033[7m", "\033[0m")))

    return wrapper


class Process:

    def __init__(self, vest_config_file):
        self.apk = None
        self.apk_temp = None
        self.vest_config = vest_config_file

    def parser_vest_list(self):
        """
        转换配置文件(会重新生成汉化版本)
        :return:
        """
        if self.vest_config is None or not os.path.exists(self.vest_config):
            return None
        vest_config_content = FilePlugin.read_str_from_file(self.vest_config)
        vest_config_content = vest_config_content.replace("A", "汉")
        vest_config_content = vest_config_content.replace("B", "H")
        vest_config_content = vest_config_content.replace("C", "1")
        new_vest_config = self.vest_config.replace(".txt", "_zh.txt")
        FilePlugin.wirte_str_to_file(vest_config_content, self.vest_config.replace(".txt", "_zh.txt"))
        return new_vest_config

    @deco
    def decode_apk_by_apktool(self):
        """
        使用apktool解包apk
        :return:
        """
        path_pro = os.path.join(constants.path_self, "pro_vestapk")
        apk_dict = FileFinder.find_file_in_cdir(path_pro, ".apk")
        if apk_dict is None or len(apk_dict) > 1:
            print("请保证当前文件夹(./pro_vestapk)有且仅有一个apk文件")
            sys.exit(0)
        self.apk = apk_dict[0]  # 不包含文件路径
        self.apk_temp = os.path.join(constants.path_self, "pro_vestapk/" + self.apk.replace(".apk", ""))
        if os.path.exists(self.apk_temp):
            # return self.apk_temp
            FilePlugin.remove_path_file(self.apk_temp)
        apk_tool_jar = os.path.join(constants.path_self, "jar/apktool.jar")
        cmd = "java -jar " + apk_tool_jar + " d " + os.path.join(path_pro, self.apk)
        print(f"执行cmd >>>> {cmd}")
        result = os.system(cmd)
        if result == 0:
            print("apktool解包成功")
            if os.path.exists(self.apk_temp):
                print(f"解包路径 >>> {self.apk_temp}")
                return self.apk_temp
        else:
            raise Exception("apktool解包失败")

    @deco
    def build_apk_by_apktool(self):
        """
        使用apktool打包新apk
        :return:
        """
        if self.apk_temp is None or not os.path.exists(self.apk_temp):
            raise FileExistsError("解包文件夹不存在")
        apk_tool_jar = os.path.join(constants.path_self, "jar/apktool.jar")
        cmd = "java -jar " + apk_tool_jar + " b " + self.apk_temp
        print(f"执行cmd >>>> {cmd}")
        result = os.system(cmd)
        if result == 0:
            print("apktool打包成功")
            rebuild_apk = os.path.join(self.apk_temp, "dist/" + self.apk)
            if os.path.exists(rebuild_apk):
                print(f"生成文件路径 >>> {rebuild_apk}")
                return rebuild_apk
        else:
            raise Exception("apktool打包执行失败")

    def replace_apk_name(self, vest_apk_name):
        """
        替换string.xml内的应用名
        :param vest_apk_name:
        :return:
        """
        strings_xml = os.path.join(self.apk_temp, "res/values/strings.xml")
        file_content = FilePlugin.read_str_from_file(strings_xml)
        old_name = re.findall(r"\"app_name\">(.+?)</string>", file_content)
        file_content = file_content.replace(old_name[0], vest_apk_name)
        FilePlugin.wirte_str_to_file(file_content, strings_xml)
        print("文件修改成功")
        pass

    def replace_apk_file_name(self, root_path, vest_apk_name):
        """
        重命名生成后的apk文件
        :param vest_apk_name:
        :return:
        """
        rebuild_apk = os.path.join(self.apk_temp, "dist/" + self.apk)
        if not os.path.exists(self.apk_temp) or not os.path.exists(rebuild_apk):
            raise FileExistsError("重命名源文件/解包文件夹 不存在")
        if not os.path.exists(root_path):
            raise FileExistsError(f"文件夹 >>> {root_path} 不存在")
        vest_apk_name = vest_apk_name.replace("汉", "A")
        vest_apk_name = vest_apk_name.replace("H", "B")
        vest_apk_name = vest_apk_name.replace("1", "C")
        new_apk = os.path.join(root_path, vest_apk_name + ".apk")
        FilePlugin.copy_file(rebuild_apk, new_apk)
        FilePlugin.remove_path_file(rebuild_apk)
        print(f"重命名至 >>> {new_apk} 成功!")

    @deco
    def sign_apk_files(self, root_path):
        apk_files = FileFinder.find_file_in_cdir(root_path, ".apk")
        jks_file = root_path.replace("base", constants.old_app_jks)
        jks_pass = "LS880617\!@#"
        sign_content = f'-alias yr -pswd {jks_pass} -aliaspswd {jks_pass}'
        for apk_file in apk_files:
            apk = os.path.join(root_path, apk_file)
            print(f'查询到需要签名的APK >>> {apk}')
            APKPlugin.signer_apk_file(jks_file, sign_content, apk)
            FilePlugin.remove_path_file(apk)

    def clear_temp(self):
        FilePlugin.remove_path_file(self.apk_temp)
        FilePlugin.remove_path_file(os.path.join(constants.path_self, "pro_vestapk/vest_config_zh.txt"))

    @deco
    def change_md5(self, path):
        FilePlugin.reset_files_md5(path)