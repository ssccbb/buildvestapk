# coding=utf-8
import os
import constants
from plugin.FilePlugin import FilePlugin

apktool = os.path.join(constants.path_self, "jar")
os.chdir(apktool)
src_file = os.path.join(constants.path_self, "pro_yrjiagu/temp_xed.apk")
tar_file = src_file.replace(".apk", "")
if os.path.exists(tar_file):
    FilePlugin.remove_path_file(tar_file)
cmd = f'java -jar apktool.jar d {src_file} -o {tar_file}'
os.system(cmd)
