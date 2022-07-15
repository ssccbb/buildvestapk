import os
import sys

import constants
from plugin.APKPlugin import APKPlugin
from plugin.FilePlugin import FilePlugin
from plugin.SearchPlugin import FileFinder
from plugin.ZipPlugin import ZipPlugin


def add_channel_file_into_apk(channel_name, meta_inf_dir):
    for root, dirs, files in os.walk(meta_inf_dir):
        for file in files:
            if file.startswith("sz"):
                FilePlugin.remove_path_file(os.path.join(meta_inf_dir, file))
    FilePlugin.wirte_str_to_file("", os.path.join(meta_inf_dir, channel_name))
    pass


def zip_channel_apk(apk_source_dir, target_apks_dir):
    ZipPlugin.make_zip_dir(source_dir=apk_source_dir, zip_file_path=target_apks_dir)
    print("zip file path >>> " + channel_apks_dir)
    pass


def sign_apk_files():
    root_path = os.path.join(constants.path_self, "pro_rechannel")
    apk_files = FileFinder.find_file_in_cdir(os.path.join(root_path, "apks"), ".apk")
    jks_file = os.path.join(root_path, "sung723.jks")
    jks_pass = "646693"
    sign_content = f'-alias sung723 -pswd {jks_pass} -aliaspswd {jks_pass}'
    for apk_file in apk_files:
        apk = os.path.join(os.path.join(root_path, "apks"), apk_file)
        print(f'查询到需要签名的APK >>> {apk}')
        APKPlugin.signer_apk_file(jks_file, sign_content, apk)
        FilePlugin.remove_path_file(apk)


if __name__ == '__main__':
    path_project = os.path.join(constants.path_self, "pro_rechannel")
    find_apks = FileFinder.find_file_in_dir(path_project, ".apk")
    if len(find_apks) != 1:
        print("请确认路径内仅有一个apk文件(命名格式xx.apk)！")
        sys.exit(0)
    # apk
    apk_file_name = find_apks[0]
    # 解压文件夹
    apk_dir = apk_file_name.replace(".apk", "")
    apk_dir = os.path.join(path_project, apk_dir)
    # 渠道文件路径
    channel_file_dir = os.path.join(apk_dir, "META-INF")
    # 改渠道之后的文件夹
    channel_apks_dir = os.path.join(path_project, "apks")
    # 解压
    FilePlugin.remove_path_file(apk_dir)
    ZipPlugin.un_zip_file(apk_file_name, apk_dir)
    # 目标渠道列表
    channel_ini = open(os.path.join(path_project, "channel.txt"), 'r', encoding='utf-8')
    for channel in channel_ini.readlines():
        # 写渠道
        channel = ("sz_" + channel).strip()
        add_channel_file_into_apk(channel_name=channel, meta_inf_dir=channel_file_dir)
        # 封包
        new_channel_apk = os.path.join(channel_apks_dir,
                                       apk_file_name.replace(".apk", "_" + channel.replace("sz_", "") + ".apk"))
        zip_channel_apk(apk_source_dir=apk_dir, target_apks_dir=new_channel_apk)
    FilePlugin.remove_path_file(apk_dir)
    sign_apk_files()
