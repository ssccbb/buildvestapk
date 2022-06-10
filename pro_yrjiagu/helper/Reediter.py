import os
import re

import constants
from plugin.FilePlugin import FilePlugin


class Reediter:

    @staticmethod
    def reedit_application_aes_ini(aes_key, aes_iv):
        """
        用于同步HookApplication内java代码和脚本(以脚本为主)AES加解密信息
        :param aes_key:
        :param aes_iv:
        :return:
        """
        path_core = os.path.join(constants.path_yrjiagu,
                                 "../pro_yrjiagu/HookApplication/Proxy_Core/src/main/java/com/proxycore/core/EncryptUtils.java")
        path_tool = os.path.join(constants.path_yrjiagu,
                                 "../pro_yrjiagu/HookApplication/Proxy_Tools/src/main/java/com/proxytools/tools/EncryptUtil.java")
        Reediter.reedit_file_aes_ini(aes_key, aes_iv, path_core)
        Reediter.reedit_file_aes_ini(aes_key, aes_iv, path_tool)
        pass

    @staticmethod
    def reedit_file_aes_ini(aes_key, aes_iv, path_file):
        """
        用于同步HookApplication内java代码和脚本(以脚本为主)AES加解密信息
        :param path_file:
        :param aes_key:
        :param aes_iv:
        :return:
        """
        # 读文件内容
        file_content = FilePlugin.read_str_from_file(path_file)
        # 查找匹配旧的字符串
        old_content = re.findall(r"byte\[\](.+?)\.getBytes", file_content)
        # 替换后的字符串
        new_iv_content = f" IV = \"{aes_iv}\""
        new_key_content = f" KEY = \"{aes_key}\""
        # 重写core包
        for content in old_content:
            if "IV" in content and content != new_iv_content:
                file_content = file_content.replace(content, new_iv_content)
            if "KEY" in content and content != new_key_content:
                file_content = file_content.replace(content, new_key_content)
        FilePlugin.wirte_str_to_file(file_content, path_file)
        pass
