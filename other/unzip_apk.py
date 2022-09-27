import os

import constants
from plugin.APKPlugin import APKPlugin
from plugin.ZipPlugin import ZipPlugin

if __name__ == '__main__':
    pro_vestapk = os.path.join(constants.path_self, "pro_vestapk")
    apk = os.path.join(pro_vestapk, "yruser_v14.6.00_2022-09-21_release_7zip_aligned_signed.apk")
    apk_obfuse = os.path.join(pro_vestapk, "npswuser_v14.3.10_2022-08-11_release_obfuse.apk")

    # apktool
    APKPlugin.unzip_apk_file(apk, apk.replace(".apk", "_apktool"))
    # APKPlugin.unzip_apk_file(apk_obfuse, apk.replace(".apk", "_apktool"))

    # zip
    # ZipPlugin.un_zip_file(apk, apk.replace(".apk", "_zip"))
    # ZipPlugin.un_zip_file(apk_obfuse, apk_obfuse.replace(".apk", "_zip"))
