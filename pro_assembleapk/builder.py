import os
import time
from pathlib import Path
from plugin.FilePlugin import FilePlugin

import constants


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


class PackageHelper:
    def __init__(self, path: str):
        print("inti package helper")
        # 安卓项目根路径
        self.path_android = path
        # 安卓项目代码路径
        self.path_android_code = self.path_android + "/app/src/main/java"
        # 安卓项目res路径
        self.path_android_res = self.path_android + "/app/src/main/res"
        # 安卓项目包路径
        self.path_android_package = self.path_android + "/app/src/main/java/com/syzdmsc/hjbm"
        # gradle.properties配置参数文件路径
        self.path_android_properties = self.path_android + "/gradle.properties"
        # 字符串文件路径
        self.path_android_string = self.path_android_res + "/values/strings.xml"
        # file_paths
        self.path_android_filepath = self.path_android_res + "/xml/file_paths.xml"

    @deco
    def check_file_change_status(self, package_name):
        dirs = package_name.split(".")
        path = self.path_android_code
        for subdir in dirs:
            if len(subdir.strip()) != 0:
                path = os.path.join(path, subdir)
        print("check >>> " + path)
        path = os.path.join(path, "wxapi")
        if os.path.exists(path) and os.listdir(path) and os.path.exists(
                os.path.join(path, "WXEntryActivity.java")) and os.path.exists(
            os.path.join(path, "WXPayEntryActivity.java")):
            print("检测到文件已做修改,即将跳过文件修改步奏...")
            return True
        print("执行文件修改步奏...")
        return False
        pass

    @staticmethod
    def query_package_name():
        """
        查询配置文件夹的包名
        :return: packagename
        """
        for sub_dir in os.listdir(constants.path_ini):
            sub_file = Path(constants.path_ini + "/" + sub_dir)
            if sub_file.is_dir():
                print("于 " + constants.path_ini + " 路径内查询到可用包名 ：" + sub_dir)
                return sub_dir
        return ""

    def change_app_name(self, app_name):
        """
        修改应用名
        :param app_name:
        :return:
        """
        print("开始替换appname ------ " + app_name)
        # path_android_string
        FilePlugin.change_str_in_file("vestname", app_name, self.path_android_string)
        FilePlugin.change_str_in_file("vestname", app_name, self.path_android_properties)
        pass

    def change_app_icon(self, path_file):
        """
        修改应用图标
        :param path_file:
        :return:
        """
        print("开始替换appicon ------ " + path_file)
        old_app_icon = self.path_android_res + "/mipmap-xxhdpi/" + constants.old_app_icon
        print("md5 >>> " + FilePlugin.md5(old_app_icon))
        FilePlugin.replace_file(old_app_icon, path_file)
        print("md5(new) >>> " + FilePlugin.md5(old_app_icon))
        print("执行完成")
        pass

    def change_app_jks(self, path_file):
        """
        修改签名文件
        :param path_file:
        :return:
        """
        print("开始替换签名文件 ------ " + path_file)
        old_app_jks = self.path_android + "/" + constants.old_app_jks
        print("md5 >>> " + FilePlugin.md5(old_app_jks))
        FilePlugin.replace_file(old_app_jks, path_file)
        print("md5(new) >>> " + FilePlugin.md5(old_app_jks))
        print("执行完成")
        pass

    @deco
    def change_app_package(self, app_package_name):
        """
        修改应用包名
        :param app_package_name:
        :return:
        """
        print("开始修改包名路径 ------ " + app_package_name)
        # properties
        self.replace_content("APP_PACKAGENAME=", app_package_name.strip(), self.path_android_properties)
        # wxapi回调包名
        app_package_name_list = app_package_name.split(".")
        new_path = self.path_android_code
        for dirname in app_package_name_list:
            new_path = new_path + "/" + dirname
        FilePlugin.rename_path(self.path_android_package, new_path)
        # com/syzdmsc/hjbm
        for root, dirs, files in os.walk(new_path):
            for subdir in dirs:
                # com/syzdmsc/hjbm/wxapi
                wxapi_dir = os.path.join(root, subdir)
                for wxapi_root, wxapi_dirs, wxapi_files in os.walk(wxapi_dir):
                    # WXEntryActivity.java
                    # WXPayEntryActivity.java
                    for wxapi_file in wxapi_files:
                        filename = os.path.join(wxapi_dir, wxapi_file)
                        if filename.endswith(".java"):
                            print("开始执行包名头部路径替换...." + filename)
                            with open(filename, mode='r') as f:
                                data = f.read()
                                f.close()
                            with open(filename, mode='w') as f:
                                content = data.replace(constants.old_app_wxapi_path, app_package_name)
                                f.write(content)
                                f.close()
        # file_path.xml
        FilePlugin.change_str_in_file(constants.old_app_package, app_package_name, self.path_android_filepath)
        pass

    @deco
    def change_random_package(self):
        """
        修改除wxapi回调代码以外的代码文件所在的包路径
        :return:
        """
        pass

    def change_app_ini(self, ini_dict):
        """
        修改其他配置参数
        :param ini_dict:
        :return:
        """
        print("开始修改其他配置参数 ------ " + str(ini_dict))
        properties_file = self.path_android_properties
        self.replace_content("APP_PACKAGENAME=", ini_dict.read_value_with_key("packageName").strip(),
                             properties_file)
        # self.replace_content("APP_VERSION=", ini_dict.read_value_with_key("versionName").strip(),
        #                               properties_file)
        # full_channel = ini_dict.read_value_with_key("channel")
        # self.replace_content("MAIN_CHANNEL=", full_channel.split("_")[0], properties_file)
        # self.replace_content("SUB_CHANNEL=", full_channel.split("_")[1], properties_file)
        self.replace_content("YD_APPID=", ini_dict.read_value_with_key("ydKey"), properties_file)
        qq_ini = ini_dict.read_value_with_key("qqKey")
        self.replace_content("QQ_APPID=", qq_ini[0].strip(), properties_file)
        self.replace_content("QQ_KEY=", qq_ini[1].strip(), properties_file)
        wechat_ini = ini_dict.read_value_with_key("wechatKey")
        self.replace_content("WECHAT_APPID=", wechat_ini[0].strip(), properties_file)
        self.replace_content("WECHAT_KEY=", wechat_ini[1].strip(), properties_file)
        # self.replace_content("KEY_OPENINSTALL=", ini_dict.read_value_with_key("openinstallKey"),
        #                      properties_file)
        self.replace_content("HIDE_SLOGAN=", str(ini_dict.read_value_with_key("hideSlogan")).lower(),
                             properties_file)
        self.replace_content("HIDE_ONEYUANDIALOG=", str(ini_dict.read_value_with_key("hideOneYuan")).lower(),
                             properties_file)
        self.replace_content("HIDE_QQLOGIN=", str(ini_dict.read_value_with_key("hideQQLogin")).lower(),
                             properties_file)
        self.replace_content("HIDE_WXLOGIN=", str(ini_dict.read_value_with_key("hideWXLogin")).lower(),
                             properties_file)
        self.replace_content("HIDE_SETTING=", str(ini_dict.read_value_with_key("hideSetting")).lower(),
                             properties_file)
        self.replace_content("HIDE_GUIDE=", str(ini_dict.read_value_with_key("hideGuide")).lower(),
                             properties_file)
        self.replace_content("HIDE_TEEN=", str(ini_dict.read_value_with_key("hideTeen")).lower(),
                             properties_file)
        self.replace_content("HIDE_PERMISSIONDIALOG=",
                             str(ini_dict.read_value_with_key("hidePermissionDialog")).lower(),
                             properties_file)
        self.replace_content("HIDE_DIALOG=", str(ini_dict.read_value_with_key("hideDialog")).lower(),
                             properties_file)
        FilePlugin.change_str_in_file("./" + constants.old_app_jks,
                                      os.path.join(self.path_android, constants.old_app_jks),
                                      os.path.join(self.path_android, "app/build.gradle"))
        print(str(properties_file) + " 配置替换完成！")
        pass

    def replace_content(self, tag, content, target_file):
        if len(tag) == 0 or len(content) == 0:
            return
        with open(target_file, mode='r') as f:
            read_lines = f.readlines()
            f.close()
        with open(target_file, mode='w') as f:
            for line in read_lines:
                if line.startswith(tag):
                    line_new = line.replace(line, tag + content)
                    if line.endswith("\n"):
                        line_new = line_new + "\n"
                    f.writelines(line_new)
                else:
                    f.writelines(line)
            f.close()
        pass

    @deco
    def change_md5(self):
        """
        重置项目内可编辑文件md5值
        :return:
        """
        # FilePlugin.reset_files_md5(self.path_android)
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

    @deco
    def encode_app_string(self):
        """
        替换加密字符串（待补全）
        :return:
        """
        pass

    @deco
    def code_rollback(self):
        """
        每次重新打包时做代码回退
        :return:
        """
        pass
