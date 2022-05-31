# coding=utf-8
import os

from pynput import keyboard
from pynput.keyboard import Key

import constants
from pro_assembleapk.builder import PackageHelper
from plugin.FilePlugin import FilePlugin
from plugin.PackagePlugin import PackageParser


def on_release(key):
    if key == Key.space:
        return False


def on_press(key):
    pass


if __name__ == '__main__':
    ini_package_name = PackageHelper.query_package_name()
    json_parser = PackageParser(ini_package_name, constants.path_ini + "/package.json")

    package_name = json_parser.read_value_with_key("packageName")
    app_name = json_parser.read_value_with_key("appName")
    version_name = json_parser.read_value_with_key("versionName")
    version_code = json_parser.read_value_with_key("versionCode")
    channel = json_parser.read_value_with_key("channel")

    yd_key = json_parser.read_value_with_key("ydKey")
    qq_ini = json_parser.read_value_with_key("qqKey")
    qq_appid = qq_ini[0]
    qq_appkey = qq_ini[1]
    wechat_ini = json_parser.read_value_with_key("wechatKey")
    wechat_appid = wechat_ini[0]
    wechat_appkey = wechat_ini[1]
    op_key = json_parser.read_value_with_key("openinstallKey")

    hide_slogan = json_parser.read_value_with_key("hideSlogan")
    hide_one_yuan = json_parser.read_value_with_key("hideOneYuan")
    hide_qq_login = json_parser.read_value_with_key("hideQQLogin")
    hide_wx_login = json_parser.read_value_with_key("hideWXLogin")
    hide_setting = json_parser.read_value_with_key("hideSetting")
    hide_guide = json_parser.read_value_with_key("hideGuide")
    hide_teen = json_parser.read_value_with_key("hideTeen")
    hide_permission_dialog = json_parser.read_value_with_key("hidePermissionDialog")
    hide_dialog = json_parser.read_value_with_key("hideDialog")

    print("开始打包前请核对以下相关包信息:")
    print(" ------- 包名：" + package_name)
    print(" ------- 应用名：" + app_name)
    print(" ------- 对外版本号：" + version_name)
    print(" ------- 对内版本号：" + version_code)
    print(" ------- 渠道：" + channel)
    print(" ------- 易盾一键登录：" + yd_key)
    print(" ------- QQ appid：" + qq_appid)
    print(" ------- QQ key：" + qq_appkey)
    print(" ------- 微信 appid：" + wechat_appid)
    print(" ------- 微信 key：" + wechat_appkey)
    print(" ------- OP：" + op_key)
    print(" ------- 隐藏包名相关UI：" + str(hide_slogan))
    print(" ------- 隐藏一元充值弹窗：" + str(hide_one_yuan))
    print(" ------- 隐藏QQ登录：" + str(hide_qq_login))
    print(" ------- 隐藏微信登录：" + str(hide_wx_login))
    print(" ------- 隐藏部分设置：" + str(hide_setting))
    print(" ------- 隐藏引导页：" + str(hide_guide))
    print(" ------- 隐藏青少年相关：" + str(hide_teen))
    print(" ------- 隐藏权限弹窗说明：" + str(hide_permission_dialog))
    print(" ------- 隐藏部分充值弹窗：" + str(hide_dialog))

    print("按任意键继续 ....")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if not PackageHelper.check_file_change_status(ini_package_name):
        # step 1 ：替换应用名
        PackageHelper.change_app_name(app_name)
        # step 2 ：替换应用图标
        PackageHelper.change_app_icon(constants.path_ini + "/" + constants.old_app_icon)
        # step 3 ：替换应用签名文件
        PackageHelper.change_app_jks(constants.path_ini + "/" + package_name + "/" + constants.old_app_jks)
        # step 4 ：更改应用包名以及wxapi回调路径包名
        PackageHelper.change_app_package(package_name)
        # step 5 ：更改其他配置相关
        PackageHelper.change_app_ini(json_parser)
    # step 6 : gradle
    print("开始执行gradle打包...")
    os.chdir(constants.path_android)
    # os.system("./gradlew aDR --offline")
    os.system("./gradlew assembleRelease")
    # step 7 : 拷贝文件
    apk_dir = os.path.join(constants.path_android, "app/build/outputs/apk/standard/release")
    for sub_file in os.listdir(apk_dir):
        if sub_file.endswith(".apk"):
            tar_dir = os.path.join(constants.path_self, "pro_assembleapk/output")
            FilePlugin.move_file(os.path.join(apk_dir, sub_file), tar_dir)
            print("apk文件已经转移至文件夹 >>> " + tar_dir)
    print("done!")
