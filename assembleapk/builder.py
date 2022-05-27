import os
from pathlib import Path
from plugin.FilePlugin import FilePlugin

import constants


class PackageHelper:
    @staticmethod
    def check_file_change_status(package_name):
        dirs = package_name.split(".")
        path = constants.path_android_code
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
        pass
        return ""

    @staticmethod
    def change_app_name(app_name):
        """
        修改应用名
        :param app_name:
        :return:
        """
        print("开始替换appname ------ " + app_name)
        # path_android_string
        FilePlugin.change_str_in_file("vestname", app_name, constants.path_android_string)
        pass

    @staticmethod
    def change_app_icon(path_file):
        """
        修改应用图标
        :param path_file:
        :return:
        """
        print("开始替换appicon ------ " + path_file)
        old_app_icon = constants.path_android_res + "/mipmap-xxhdpi/" + constants.old_app_icon
        print("md5 >>> " + FilePlugin.md5(old_app_icon))
        FilePlugin.replace_file(old_app_icon, path_file)
        print("md5(new) >>> " + FilePlugin.md5(old_app_icon))
        print("执行完成")
        pass

    @staticmethod
    def change_app_jks(path_file):
        """
        修改签名文件
        :param path_file:
        :return:
        """
        print("开始替换签名文件 ------ " + path_file)
        old_app_jks = constants.path_android + "/" + constants.old_app_jks
        print("md5 >>> " + FilePlugin.md5(old_app_jks))
        FilePlugin.replace_file(old_app_jks, path_file)
        print("md5(new) >>> " + FilePlugin.md5(old_app_jks))
        print("执行完成")
        pass

    @staticmethod
    def change_app_package(app_package_name):
        """
        修改应用包名
        :param app_package_name:
        :return:
        """
        print("开始修改包名路径 ------ " + app_package_name)
        # properties
        PackageHelper.replace_content("APP_PACKAGENAME=", app_package_name.strip(), constants.path_android_properties)
        # wxapi回调包名
        app_package_name_list = app_package_name.split(".")
        new_path = constants.path_android_code
        for dirname in app_package_name_list:
            new_path = new_path + "/" + dirname
        FilePlugin.rename_path(constants.path_android_package, new_path)
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
        FilePlugin.change_str_in_file(constants.old_app_package, app_package_name, constants.path_android_filepath)
        pass

    @staticmethod
    def change_app_ini(ini_dict):
        """
        修改其他配置参数
        :param ini_dict:
        :return:
        """
        print("开始修改其他配置参数 ------ " + str(ini_dict))
        properties_file = constants.path_android_properties
        PackageHelper.replace_content("APP_PACKAGENAME=", ini_dict.read_value_with_key("packageName").strip(),
                                      properties_file)
        # PackageHelper.replace_content("APP_VERSION=", ini_dict.read_value_with_key("versionName").strip(),
        #                               properties_file)
        # full_channel = ini_dict.read_value_with_key("channel")
        # PackageHelper.replace_content("MAIN_CHANNEL=", full_channel.split("_")[0], properties_file)
        # PackageHelper.replace_content("SUB_CHANNEL=", full_channel.split("_")[1], properties_file)
        PackageHelper.replace_content("YD_APPID=", ini_dict.read_value_with_key("ydKey"), properties_file)
        qq_ini = ini_dict.read_value_with_key("qqKey")
        PackageHelper.replace_content("QQ_APPID=", qq_ini[0].strip(), properties_file)
        PackageHelper.replace_content("QQ_KEY=", qq_ini[1].strip(), properties_file)
        wechat_ini = ini_dict.read_value_with_key("wechatKey")
        PackageHelper.replace_content("WECHAT_APPID=", wechat_ini[0].strip(), properties_file)
        PackageHelper.replace_content("WECHAT_KEY=", wechat_ini[1].strip(), properties_file)
        PackageHelper.replace_content("KEY_OPENINSTALL=", ini_dict.read_value_with_key("openinstallKey"),
                                      properties_file)
        PackageHelper.replace_content("HIDE_SLOGAN=", str(ini_dict.read_value_with_key("hideSlogan")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_ONEYUANDIALOG=", str(ini_dict.read_value_with_key("hideOneYuan")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_QQLOGIN=", str(ini_dict.read_value_with_key("hideQQLogin")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_WXLOGIN=", str(ini_dict.read_value_with_key("hideWXLogin")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_SETTING=", str(ini_dict.read_value_with_key("hideSetting")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_GUIDE=", str(ini_dict.read_value_with_key("hideGuide")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_TEEN=", str(ini_dict.read_value_with_key("hideTeen")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_PERMISSIONDIALOG=",
                                      str(ini_dict.read_value_with_key("hidePermissionDialog")).lower(),
                                      properties_file)
        PackageHelper.replace_content("HIDE_DIALOG=", str(ini_dict.read_value_with_key("hideDialog")).lower(),
                                      properties_file)
        FilePlugin.change_str_in_file("./" + constants.old_app_jks,
                                      os.path.join(constants.path_android, constants.old_app_jks),
                                      os.path.join(constants.path_android, "app/build.gradle"))
        print(str(properties_file) + " 配置替换完成！")
        pass

    @staticmethod
    def replace_content(tag, content, target_file):
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
