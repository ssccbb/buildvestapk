# coding=utf-8
# 查找字符串
import os
import re
import sys

import constants
from plugin.FilePlugin import FilePlugin
from plugin.DictPlugin import *


# 需要xmlclassproguard插件支持
# 这个插件易用性相当差每回改完会有很多遗漏及错误 别用
class Finder:

    def __init__(self):
        self.file_names = []
        self.dir_names = []
        self.dir_new_names = {}
        self.ignore_name = {'android', 'test', 'v7', 'syzdmsc', 'hjbm', 'aop', 'androidTest'}
        self.package_names = {}

    def find_same_name_class(self, module_path):
        """
        查找根目录存在的同名文件（不同路径同名字）以及同名文件（不同路径同名字）
        :param module_path:
        :return:
        """
        for root, dirs, files in os.walk(module_path):
            for file in files:
                if file in self.file_names:
                    print(f'已存在文件 {os.path.join(root, file)}')
                else:
                    self.file_names.append(file)
            for dir in dirs:
                path_dir = os.path.join(root, dir)
                package = path_dir[path_dir.index("/java/") + 6:len(path_dir)]
                if package in self.dir_names:
                    print(
                        f'已存在路径 {package}        ({path_dir[path_dir.index("/huajian-android/") + 17:len(path_dir)]})')
                else:
                    self.dir_names.append(package)
        pass

    def pre_build_dirs(self, module_path):
        """
        递归module文件夹生成每个文件夹名字的对应表
        :param module_path:
        :return:
        """
        if not os.path.exists(module_path):
            return
        if module_path not in self.dir_new_names.keys():
            self.dir_new_names.update({module_path: {}})
        name_map = self.dir_new_names.get(module_path)
        self.pre_build_sub_dirs(module_path, name_map)
        self.dir_new_names.update({module_path: name_map})
        pass

    def pre_build_sub_dirs(self, path_dir, name_map):
        """
        用于方法 pre_build_dirs(self, module_path): 递归查找自文件夹
        :param path_dir:
        :param name_map:
        :return:
        """
        for path in os.listdir(path_dir):
            real_path = os.path.join(path_dir, path)
            if not os.path.exists(real_path) or os.path.isfile(real_path) or path in self.ignore_name:
                continue
            new_name = DictPlugin.random_string(1)[0]
            while new_name in name_map.values():
                new_name = DictPlugin.random_string(1)[0]
            name_map.update({path: new_name})
            self.pre_build_sub_dirs(real_path, name_map)
        pass

    def reset_gradle(self, module_path):
        """
        重定义build.gradle内的包名对应新路径
        需要结合xmlclassguard的插件一起使用
        :return:
        """
        if not os.path.exists(module_path):
            return None
        values = ''
        # 每循环完一个module清空一次
        self.package_names = {}
        print(f'开始处理module路径 {module_path}')
        self.pre_build_dirs(module_path)
        name_map = self.dir_new_names.get(module_path)
        self.rename_sub_path(module_path, name_map)
        # 更改配置字段moveDir
        for old in self.package_names.keys():
            count = len(old.split("/"))
            # 控制一下需要混淆的层级
            # 默认混淆从第三层级开始 一二层级同名概率教大com.yr
            # 层级过多会导致写入gradle内的配置长度过长编译不通过
            # 层级数不做更改 原本几级更改后还是几级
            if 3 > count or count > 8:
                continue
            values = values + f'\t\t"{old}"\t:\t"{self.package_names.get(old)}",\n'
        return values

    def rename_sub_path(self, path_dir, name_map):
        """
        用于方法 reset_gradle(self, module_path): 递归查自文件夹
        :param path_dir:
        :param name_map:
        :return:
        """
        for path in os.listdir(path_dir):
            real_path = os.path.join(path_dir, path)
            if not os.path.exists(real_path) or os.path.isfile(real_path) or path in self.ignore_name:
                continue
            old_package = (real_path[(real_path.index('main/java') + 9 if 'main/java' in real_path else real_path.index('/src/') + 5):len(real_path)]).strip().lstrip()
            if old_package.startswith('/'):
                old_package = old_package[1:len(old_package)]
            new_package = ''
            for package in old_package.split('/'):
                if package in name_map.keys():
                    new_package = (new_package + '/' + name_map.get(package)).strip().lstrip()
                else:
                    new_package = (new_package + '/' + package).strip().lstrip()
            if new_package.startswith('/'):
                new_package = new_package[1:len(new_package)]
            print(f'{old_package} ==== {new_package}')
            self.package_names.update({old_package: new_package})
            self.rename_sub_path(real_path, name_map)


"""
查找位于 app/build.gradle 文件内的 xmlclassguard 的配置
遍历所有 module 包包路径重新生成随机包名并修改配置
此方法只做一键生成 moveDir 配置，package的包名修改需要手动对照 AndroidMainfest 
内定义的 package 字段修，修改完成直接运行 gradlew.task#moveDir 即可
"""
if __name__ == '__main__':
    # print(str(FilePlugin.is_string_in_path("com.yr.network", os.path.join(constants.path_android_code, "com/yr/network"))))
    android_dir = os.path.join(constants.path_root, "flutter-project/huajian-android")
    target_dir = [
        os.path.join(android_dir, "app/src/main/java"),
        # os.path.join(android_dir, "library-beauty/src/main/java"),
        os.path.join(android_dir, "library-commonlib/src/main/java"),
        os.path.join(android_dir, "library-eventbus/src/main/java"),
        os.path.join(android_dir, "library-im/src/main/java"),
        # os.path.join(android_dir, "commonlibrary/src/main/java"),
        os.path.join(android_dir, "module-community/src/main/java"),
        os.path.join(android_dir, "module-ext/src/main/java"),
        os.path.join(android_dir, "module-live/src/main/java"),
        # os.path.join(android_dir, "module-message/src/"),
        os.path.join(android_dir, "module-party/src/main/java"),
        os.path.join(android_dir, "module-vchat/src/main/java"),
        os.path.join(android_dir, "YR-Network/src/main/java"),
        os.path.join(android_dir, "YR-Player/src/main/java"),
        # os.path.join(android_dir, "YR-SvgaImage/src/main/java"),
        os.path.join(android_dir, "YR-Tools/src/main/java"),
        os.path.join(android_dir, "YR-Uikit/src/main/java")
    ]
    finder = Finder()
    # 查找同名文件 同名com/xxxx路径
    move_dir_values = ''
    for dirs in target_dir:
        # finder.find_same_name_class(dirs)
        result = finder.reset_gradle(dirs)
        if result is not None:
            move_dir_values = move_dir_values + result
    move_dir_values = '[\n' + move_dir_values[0:move_dir_values.rindex(',')].replace("/", ".") + '\n]'
    print(f'生成的包对应关系表为：')
    print(move_dir_values)
    gradle_path = os.path.join(android_dir, "app/build.gradle")
    gradle_content = FilePlugin.read_str_from_file(gradle_path)
    # 更改 packageChange = ["com.yr.huajian" : "ncwhde.ycmurn.snplte"]
    # result1 = re.compile('packageChange\\s+=\\s+(\\[([\\w\\s\\n\\.:,"]+)\\])', re.M).search(gradle_content)
    # if result1 is not None:
    #     new_package = ''
    #     match_str1 = result1.group().lstrip().strip()
    #     for name in match_str1[match_str1.index('[') + 1:match_str1.index(']')].split(':')[0].replace('"','').split('.'):
    #         if name in finder.dir_new_names.keys():
    #             new_package = new_package+'.'
    #         else:
    #             new_package = ''
    #             break
    #     if len(new_package) > 0:
    #         gradle_content = gradle_content.replace(match_str1, f'packageChange = ["com.yr.huajian" : "{new_package[0,len(new_package)-1]}"]')
    # 更改 moveDir = ["com" : "ncwhde"]
    result = re.compile('moveDir\\s+=\\s+(\\[([\\w\\s\\n\\.:,"]+)\\])', re.M).search(gradle_content)
    if result is None:
        print(f'未查找到 moveDir = [.*] 的配置 ...')
        sys.exit(0)
    match_str = result.group().lstrip().strip()
    gradle_content = gradle_content.replace(match_str, 'moveDir = ' + move_dir_values)
    # 重写 gradle
    FilePlugin.wirte_str_to_file(gradle_content, gradle_path)
    print('gradle配置修改完成！')
