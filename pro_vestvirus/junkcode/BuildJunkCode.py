import os
import re
import sys
import shutil
import constants
from plugin.FilePlugin import *
from pro_assembleapk.Git import Git


class Builder:

    def __init__(self, source_dir, package_name):
        print('开始生成垃圾代码....')
        print(f'{package_name}')
        self.package_name = package_name
        self.junk_dir = os.path.join(constants.path_root, "android-project/JunkCode")
        self.junk_code = os.path.join(self.junk_dir, 'app/build/generated/source/junk')
        self.junk_code_package = self.match_package(self.junk_dir)
        self.target_dir = source_dir
        self.target_code_package = self.match_package(self.target_dir)

    @staticmethod
    def match_package(path_root: str):
        main_fest_content = FilePlugin.read_str_from_file(os.path.join(path_root, 'app/src/main/AndroidManifest.xml'))
        split = main_fest_content[main_fest_content.index('<manifest'):len(main_fest_content)]
        package = split[split.index('package'):split.index('>') + 1]
        return re.compile('\\".*\\"', re.M).search(package).group().replace('"', '').strip().lstrip()

    def creat_junk(self):
        """
        以新建的方式插入文件到所定义的包名路径内
        :return:
        """
        if self.package_name is None or len(self.package_name) == 0:
            print('package_name 未正确定义')
            sys.exit(0)
            return
        FilePlugin.remove_path(os.path.join(self.junk_dir, 'app/build'))
        self.pre_change_package()
        self.excute_gradle()
        if not self.check_code():
            print(f'垃圾代码未生成 === {self.junk_code}')
            return
        self.remove_to_target()
        # 回退代码
        # git = Git(self.junk_dir)
        # git.remove_local_change()
        print(f'执行完成')

    def pre_change_package(self):
        # 修改关联包名
        # packageBase = "com.yr.jksdemo"
        path_gradle = os.path.join(self.junk_dir, 'app/build.gradle')
        file_content = FilePlugin.read_str_from_file(path_gradle)
        old_str = re.compile('packageBase = ".*"').search(file_content).group().lstrip().strip()
        file_content = file_content.replace(old_str, f'packageBase = "{self.package_name}"')
        FilePlugin.wirte_str_to_file(file_content, path_gradle)

    def excute_gradle(self):
        print("开始执行gradle打包...")
        os.chdir(self.junk_dir)
        os.system("./gradlew assembleRelease")

    def check_code(self):
        if not os.path.exists(self.junk_code):
            return False
        return True

    def rewrite_import(self, path: str):
        """
        重新更改import R & BuildConfig
        :param path:
        :return:
        """
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if 'activity' not in file.lower():
                        continue
                    file_path = os.path.join(root, file)
                    file_content = FilePlugin.read_str_from_file(file_path)
                    file_content = file_content.replace(f'{self.junk_code_package}.R', f'{self.target_code_package}.R')
                    file_content = file_content.replace(f'{self.junk_code_package}.BuildConfig', f'{self.target_code_package}.BuildConfig')
                    FilePlugin.wirte_str_to_file(file_content, file_path)
        elif os.path.isfile(path):
            file_content = FilePlugin.read_str_from_file(path)
            file_content = file_content.replace(f'{self.junk_code_package}.R', f'{self.target_code_package}.R')
            file_content = file_content.replace(f'{self.junk_code_package}.BuildConfig',
                                                f'{self.target_code_package}.BuildConfig')
            FilePlugin.wirte_str_to_file(file_content, path)
        pass

    def remove_to_target(self):
        package_dict = self.package_name.replace(".", "/")
        # java
        print(f'开始移动java文件')
        path_java = os.path.join(self.junk_code, f'release/java/{package_dict}')
        path_java_target = os.path.join(self.target_dir, f'app/src/main/java/{package_dict}')
        if os.path.exists(path_java_target):
            for root, dirs, files in os.walk(path_java):
                for dirz in dirs:
                    new_path = os.path.join(root, dirz)
                    new_path_target = os.path.join(path_java_target, dirz)
                    if os.path.exists(new_path_target):
                        print(f'目标文件夹存在,请手动处理 ==== {new_path_target}')
                    else:
                        self.rewrite_import(new_path)
                        shutil.move(new_path, new_path_target)
        else:
            self.rewrite_import(path_java)
            shutil.move(path_java, path_java_target)
        # drawable
        print(f'开始移动图片文件')
        path_drawable = os.path.join(self.junk_code, f'release/res/drawable')
        path_drawable_target = os.path.join(self.target_dir, f'app/src/main/res/drawable')
        for root, dirs, files in os.walk(path_drawable):
            for file in files:
                drawable = os.path.join(root, file)
                new_drawable = os.path.join(path_drawable_target, file)
                if os.path.exists(new_drawable):
                    print(f'目标图片文件存在,请手动处理 ==== {drawable}')
                else:
                    FilePlugin.move_file(drawable, new_drawable)
        # layout
        print(f'开始移动布局文件')
        path_layout = os.path.join(self.junk_code, f'release/res/layout')
        path_layout_target = os.path.join(self.target_dir, f'app/src/main/res/layout')
        for root, dirs, files in os.walk(path_layout):
            for file in files:
                layout = os.path.join(root, file)
                new_layout = os.path.join(path_layout_target, file)
                if os.path.exists(new_layout):
                    print(f'目标布局文件存在,请手动处理 ==== {layout}')
                else:
                    FilePlugin.move_file(layout, new_layout)
        # AndroidMainfest.xml
        print(f'开始修改清单文件')
        path_mainfest = os.path.join(self.junk_code, f'release/AndroidManifest.xml')
        path_mainfest_target = os.path.join(self.target_dir, f'app/src/main/AndroidManifest.xml')
        mainfest_content = FilePlugin.read_str_from_file(path_mainfest)
        FilePlugin.change_str_in_file("</application>", ("\n" + mainfest_content[mainfest_content.index(
            "<activity android:name="):mainfest_content.rindex("</application>")] + "\n</application>"),
                                      path_mainfest_target)
        # strings.xml
        print(f'开始修改strings文件')
        path_strings = os.path.join(self.junk_code, f'release/res/values/strings.xml')
        path_strings_target = os.path.join(self.target_dir, f'app/src/main/res/values/strings.xml')
        strings_content = FilePlugin.read_str_from_file(path_strings)
        FilePlugin.change_str_in_file("</resources>", ("\n" + strings_content[strings_content.index(
            "<string name="):strings_content.rindex("</resources>")] + "\n</resources>"),
                                      path_strings_target)
        # proguard.pro
        print(f'开始修改混淆文件')
        path_proguard = os.path.join(self.target_dir, 'app/proguard-rules.pro')
        proguard_content = FilePlugin.read_str_from_file(path_proguard).strip()
        proguard_content = proguard_content + f'\n{self.pre_build_proguard()}'
        FilePlugin.wirte_str_to_file(proguard_content, path_proguard)
        pass

    def pre_build_proguard(self):
        # 生成混淆代码
        return '-keep class packagename.** {*;}'.replace('packagename', self.package_name)
