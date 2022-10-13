import re

from plugin.DictPlugin import DictPlugin
from pro_vestvirus.encrypt.AES import AES
from pro_vestvirus.junkcode.BuildJunkCode import *
from plugin.FilePlugin import *
import constants
import os
from pro_vestvirus.stringsxml.FindInStringsXML import *


class Process:

    def __init__(self, path_android):
        self.path_android = path_android
        self.path_root = constants.path_vest_virus

    def build_junk_code_with_gradle(self):
        """
        生成垃圾代码到app包内,独立包名不混在旧包路径内
        :return:
        """
        dict_ = DictPlugin.random_string(2)
        builder = Builder(self.path_android, f'com.{dict_[0]}.{dict_[1]}')
        builder.creat_junk()
        pass

    def rewrite_pic_to_same(self):
        """
        覆盖所有图片文件为同一张图片
        :return:
        """
        source_png = os.path.join(self.path_root, "pic/a.png")
        source_9png = os.path.join(self.path_root, "pic/b.9.png")
        source_webp = os.path.join(self.path_root, "pic/c.webp")
        target_dir = [
            os.path.join(self.path_android, "app/src/main/res"),
            os.path.join(self.path_android, "app/src/main/res-umc"),
            os.path.join(self.path_android, "app/src/main/res-umc"),
            os.path.join(self.path_android, "library-beauty/src/main/res"),
            os.path.join(self.path_android, "library-commonlib/src/main/res"),
            os.path.join(self.path_android, "library-eventbus/src/main/res"),
            os.path.join(self.path_android, "library-im/src/main/res"),
            os.path.join(self.path_android, "module-community/src/main/res"),
            os.path.join(self.path_android, "module-ext/src/main/res"),
            os.path.join(self.path_android, "module-live/src/main/res"),
            os.path.join(self.path_android, "module-message/src/main/res"),
            os.path.join(self.path_android, "module-party/src/main/res"),
            os.path.join(self.path_android, "module-vchat/src/main/res"),
            os.path.join(self.path_android, "YR-Network/src/main/res"),
            os.path.join(self.path_android, "YR-Player/src/main/res"),
            os.path.join(self.path_android, "YR-SvgaImage/src/main/res"),
            os.path.join(self.path_android, "YR-Tools/src/main/res"),
            os.path.join(self.path_android, "YR-Uikit/src/main/res")
        ]
        pic_dir = ['drawable', 'drawable-hdpi', 'drawable-xhdpi', 'drawable-xxhdpi', 'mipmap-hdpi', 'mipmap-mdpi',
                   'mipmap-xhdpi', 'mipmap-xxhdpi', 'mipmap-xxxhdpi']
        for path_root in target_dir:
            if not os.path.exists(path_root):
                print(f'文件夹不存在  --> {path_root}')
                continue
            for path_sub_dir in pic_dir:
                path_target = os.path.join(path_root, path_sub_dir)
                if not os.path.exists(path_target):
                    print(f'文件夹不存在  --> {path_target}')
                    continue
                print(f'以下是全部文件 （{path_target})')
                for root, dirs, files in os.walk(path_target):
                    for file in files:
                        path_file = os.path.join(root, file)
                        if FilePlugin.is_pic_file(path_file):
                            FilePlugin.remove_path_file(path_file)
                            FilePlugin.copy_file(source_png, path_file)
                        if path_file.endswith('.9.png'):
                            FilePlugin.remove_path_file(path_file)
                            FilePlugin.copy_file(source_9png, path_file)
                        if path_file.endswith('.webp'):
                            FilePlugin.remove_path_file(path_file)
                            FilePlugin.copy_file(source_webp, path_file)
        print(f'处理完成！')
        pass

    def remove_unuse_strings_in_xml(self):
        """
        移除strings.xml内用不到的字符串
        :return:
        """
        finder = Finder(self.path_android)
        finder.deal_strings_xml()

    def rewrite_string_value_in_xml(self):
        """
        所有module内strings.xml字符串全部换成a
        :return:
        """
        paths = [os.path.join(self.path_android, 'app/src/main/res/values/strings.xml'),
                 os.path.join(self.path_android, 'library-commonlib/src/main/res/values/strings.xml'),
                 os.path.join(self.path_android, 'library-im/src/main/res/values/strings.xml'),
                 os.path.join(self.path_android, 'module-community/src/main/res/values/strings.xml'),
                 os.path.join(self.path_android, 'module-message/res/values/strings.xml')]
        # 把所有字符串替换成a
        for path in paths:
            file_content = open(path, "r").readlines()
            for line in file_content:
                method_match = re.compile('>.*<', re.M).search(line)
                new_line = ''
                if method_match is not None:
                    result = method_match.group().strip()
                    new_line = line.replace(result, '>a<')
                FilePlugin.change_str_in_file(line, new_line, path)
        pass

    def change_file_md5(self):
        """
        重置项目内可编辑文件md5值
        :return:
        """
        # FilePlugin.reset_files_md5(root_path)
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "app"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "library-beauty"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "library-commonlib"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "library-eventbus"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "library-im"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-community"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-ext"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-live"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-message"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-party"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "module-vchat"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "YR-Network"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "YR-Player"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "YR-SvgaImage"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "YR-Tools"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "YR-Uikit"))
        FilePlugin.reset_files_md5(os.path.join(self.path_android, "commonlibrary"))
        pass

    def rewrite_encrypt_string(self):
        """
        重新定义aes加密,替换项目内用到的加密后的字符串
        :return:
        """
        print(f'开始重置加密串')
        aes = AES(self.path_android)
        # 替换UseForBaoDu.java加密串
        file_content = FilePlugin.read_str_from_file(aes.path_target_file)
        for result in re.compile(aes.params_regular, re.M).finditer(file_content):
            if result is None:
                continue
            result = result.group().lstrip().strip()
            params_value = result[result.index('"') + 1:result.rindex('"')]
            new_value = aes.get_new_encrypt_string(params_value)
            if new_value is not None:
                file_content = file_content.replace(params_value, new_value)
        FilePlugin.wirte_str_to_file(file_content, aes.path_target_file)
        print(f'重写 UseForBaoDu.java 成功')
        # 重写txt文件
        for file in aes.path_files:
            file_content = FilePlugin.read_str_from_file(file)
            FilePlugin.wirte_str_to_file(aes.get_new_encrypt_string(file_content), file)
            print(f'重写 {file} 成功')
        # 重写config.gradle文件
        config_content = FilePlugin.read_str_from_file(aes.path_gradle)
        config_result = re.compile(f'key\s+=\s+', re.M).search(config_content)
        if config_result is not None:
            result = config_content[config_content.index(config_result.group().lstrip().strip()):len(config_content)]
            result = result[0:result.index(']')]
            config_result_dict = result.split(',')
            for config_keys in config_result_dict:
                if 'yrAppKey' in config_keys or 'yrAppId' in config_keys \
                        or 'nimKey' in config_keys or 'umengKey' in config_keys:
                    old_key = config_keys.split(':')[1].lstrip().strip().replace('"', '')
                    config_content = config_content.replace(old_key, aes.get_new_encrypt_string(old_key))
            FilePlugin.wirte_str_to_file(config_content, aes.path_gradle)
            print(f'重写 config.gradle 成功')
        # 重写app/build.gradle文件
        app_gradle_content = FilePlugin.read_str_from_file(aes.path_app_gradle)
        for app_gradle_str in re.compile(f'aesDecoder\\(\\".*\\"\\)', re.M).finditer(app_gradle_content):
            app_gradle_str = app_gradle_str.group().lstrip().strip().replace('aesDecoder("', '').replace('")', '')
            app_gradle_content = app_gradle_content.replace(app_gradle_str, aes.get_new_encrypt_string(app_gradle_str))
        FilePlugin.wirte_str_to_file(app_gradle_content, aes.path_app_gradle)
        print(f'重写 app/build.gradle 成功')
        # 重写gradle.properties文件
        properties_content = FilePlugin.read_str_from_file(aes.path_properties)
        for line in open(aes.path_properties, 'r'):
            new_line = None
            if 'KEY_OPENINSTALL' in line:
                new_line = 'KEY_OPENINSTALL=' + aes.get_new_encrypt_string(
                    line.replace('KEY_OPENINSTALL=', '').replace('"', '').strip()) + '\n'
            if 'MAIN_CHANNEL' in line:
                new_line = 'MAIN_CHANNEL="' + aes.get_new_encrypt_string(
                    line.replace('MAIN_CHANNEL=', '').replace('"', '').strip()) + '"\n'
            if 'SUB_CHANNEL' in line:
                new_line = 'SUB_CHANNEL="' + aes.get_new_encrypt_string(
                    line.replace('SUB_CHANNEL=', '').replace('"', '').strip()) + '"\n'
            if new_line is None or len(new_line) <= 0:
                continue
            properties_content = properties_content.replace(line, new_line)
        FilePlugin.wirte_str_to_file(properties_content, aes.path_properties)
        print(f'重写 gradle.properties 成功')
        # 替换key
        FilePlugin.wirte_str_to_file(
            FilePlugin.read_str_from_file(aes.path_gradle).replace(aes.old_aes_key, aes.new_aes_key), aes.path_gradle)
        print(f'重写 aes_key 成功')
        pass

    def rewrite_string_fog(self):
        aes = AES(self.path_android)
        app_gradle_content = FilePlugin.read_str_from_file(aes.path_app_gradle)
        match = re.compile("key\\s\\'\\w+\\'", re.M).search(app_gradle_content)
        if match is not None:
            key = match.group().strip().lstrip()
            new_key = DictPlugin.random_string_full(18)
            app_gradle_content = app_gradle_content.replace(key, f'key \'{new_key}\'')
            FilePlugin.wirte_str_to_file(app_gradle_content, aes.path_app_gradle)
            print(f'修改stringfog密钥成功！===={new_key}')
        else:
            print(f'修改stringfog密钥失败')
        pass
