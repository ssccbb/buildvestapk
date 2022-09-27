# coding=utf-8

# 重写项目包名路径
import os
import re
import constants
from plugin.FilePlugin import *
from plugin.DictPlugin import *
from pro_codeanalysis.Regular import *


class RewritePackage:

    def __init__(self, root_path):
        self.path = os.path.join(root_path, "src/main/java/com")
        self.mainfest_path = os.path.join(root_path, "src/main/AndroidManifest.xml")
        self.dir_count = FilePlugin.count_dir(self.path)
        self.file_count = 0
        self.name = DictPlugin.random_string(self.dir_count + 1)
        self.package = {}
        # 文件路径修改前后对比
        self.file_paths = []
        # 自动生成的R类和BuildConfig在的包名
        self.auto_package = ""

    def record_file_struct(self, path_dir):
        """
        记录文件结构
        :param path_dir:
        :return:
        """
        for file in os.listdir(path_dir):
            f = os.path.join(path_dir, file)
            if os.path.isfile(f):
                self.file_count += 1
                # 记录文件路径
                new_file = file.split(".")[0]
                new_package = f[f.find("/com/") + 1:f.rfind("/")].replace("/", ".")
                if new_package in self.package.keys():
                    values = self.package.get(new_package)
                    if values is None:
                        values = {"newname": "", "files": [new_file]}
                    else:
                        if values.get("files") is None:
                            values.update({"newname": "", "files": [new_file]})
                        else:
                            values["files"] = values.get("files") + [new_file]
                    self.package[new_package] = values
                else:
                    values1 = {"newname": "", "files": [new_file]}
                    self.package.update({new_package: values1})
            elif os.path.isdir(f):
                self.record_file_struct(f)
        pass

    def record_file_struct_after_edit(self, path_dir):
        """
        在重命名完文件夹之后重写记录新的文件夹名
        :param path_dir:
        :return:
        """
        for file in os.listdir(path_dir):
            f = os.path.join(path_dir, file)
            if os.path.isfile(f):
                new_file = file.split(".")[0]
                new_package = f[f.find("/com/") + 1:f.rfind("/")].replace("/", ".")
                for key in self.package.keys():
                    values = self.package.get(key)
                    if values is not None:
                        new_files = values.get("files")
                        if new_file in new_files:
                            if len(key.split(".")) == len(new_package.split(".")) and len(values.get("newname")) == 0:
                                values["newname"] = new_package
            elif os.path.isdir(f):
                self.record_file_struct_after_edit(f)
        pass

    def rename_dir(self, path_dir):
        """
        重命名文件夹
        :param path_dir:
        :return:
        """
        # print(f'处理文件夹--->{path_dir}')
        for file in os.listdir(path_dir):
            f = os.path.join(path_dir, file)
            if os.path.isdir(f):
                self.dir_count -= 1
                print(f'待重命名文件夹数剩余： {self.dir_count}')
                # 重命名文件夹
                f_dict = f.split("/")
                new_name = self.name[0]
                new_f = f[0:len(f) - len(f_dict[len(f_dict) - 1])] + new_name
                self.name.remove(new_name)
                FilePlugin.rename_path(f, new_f)
                # 递归读文件夹
                self.rename_dir(new_f)
        # print("结束-----")
        pass

    def rename_file(self, path_dir):
        """
        修改文件
        :param path_dir:
        :return:
        """
        for file in os.listdir(path_dir):
            f = os.path.join(path_dir, file)
            if os.path.isfile(f):
                self.file_count -= 1
                print(f'待处理文件数剩余： {self.file_count}')
                self.rename_file_content(f)
            elif os.path.isdir(f):
                self.rename_file(f)
        pass

    def rename_file_content(self, file):
        """
        修改单个文件内容
        :param file:
        :return:
        """
        # print(f'处理文件----->{file}')
        # print(f'开始改package')
        result = re.compile('/com/', re.M).search(file).group().strip().lstrip()
        result = result[1:len(result)]
        path_dict = result.split("/")
        package = result.replace("/" + path_dict[len(path_dict) - 1], "").replace("/", ".")
        # 读文件
        f = FilePlugin.read_str_from_file(file).lstrip().strip()
        if f is None or len(f) == 0:
            return
        # 重写package头
        head = re.compile(Regular.r_head_package(), re.M).search(f)
        if head is not None:
            f = f.replace(head.group().strip().lstrip(), f'package {package};')
        # print(f'开始改import')
        result = re.compile(Regular.r_import(), re.M).finditer(f)
        if result is None:
            return
        for group in result:
            package = group.group()
            import_package = package.strip().lstrip()[6:len(package.lstrip().strip())].lstrip().strip().replace(";", "")
            import_file = import_package[import_package.rfind(".") + 1:len(import_package)]
            for key in self.package.keys():
                if key in import_package and import_file in self.package.get(key).get("files"):
                    new_import = package.replace(import_package,
                                                 self.package.get(key).get("newname") + "." + import_file)
                    f = f.replace(package, new_import)
                    # print(f'原始字符串：{package}\t新的字符串：{new_import}')
                    continue
                if import_file == "R" or import_file == "BuildConfig":
                    if import_package.replace(("." + import_file), "") in key:
                        if self.auto_package is None or len(self.auto_package) == 0:
                            new_import_r = ""
                            for name in self.package.get(key).get("newname").split(".")[
                                        0:len(import_package.split(".")) - 1]:
                                new_import_r += (name + ".")
                            self.auto_package = new_import_r[0:len(new_import_r) - 1]
                        if self.auto_package is not None and len(self.auto_package) > 0:
                            f = f.replace(package, package.replace(import_package, self.auto_package + (
                                "R" if import_file == ".R" else ".BuildConfig")))
                        # print(f'原始字符串：{package}\t新的字符串：{new_import}.R')
                        continue
        FilePlugin.wirte_str_to_file(f, file)
        # print("结束-----")
        pass

    def rename_mainfest_content(self):
        if not os.path.exists(self.mainfest_path):
            print(f'AndroidManifest.xml文件不存在（{self.mainfest_path}）')
            return
        mainfest = FilePlugin.read_str_from_file(self.mainfest_path)
        # 匹配修改项目
        package_head = re.compile(f'package="{Regular.r_package()}">', re.M).search(mainfest)
        activtiy_name = []
        for activtiy in re.compile('<(activity|service|application)[\\n\\t\\s]+android:name="[\\w\\.]+"',
                                   re.M).finditer(mainfest):
            activtiy_name.append(activtiy.group().lstrip().strip())
        for target in re.compile('android:targetActivity=".*">', re.M).finditer(mainfest):
            activtiy_name.append(target.group().lstrip().strip())
        # 去掉package
        if package_head is not None:
            mainfest = mainfest.replace(package_head.group().lstrip().strip(), ">")
        # 改class路径（全路径可以不依赖package）
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                for name in activtiy_name:
                    path = name.split('"')[1]
                    path_dict = path.split(".")
                    if file_path.split(".")[0].endswith(path_dict[len(path_dict) - 1]):
                        new_path = file_path[file_path.index("/com/") + 1:len(file_path)].split(".")[0].replace("/",
                                                                                                                ".")
                        mainfest = mainfest.replace(name, name.replace(path, new_path))
                        activtiy_name.remove(name)
        FilePlugin.wirte_str_to_file(mainfest, self.mainfest_path)
        pass

    def rename_layout_content(self):
        xml_path = self.path.replace("java/com", "res/layout")
        for root, dirs, files in os.walk(xml_path):
            for file in files:
                xml_content = FilePlugin.read_str_from_file(file)

        pass
