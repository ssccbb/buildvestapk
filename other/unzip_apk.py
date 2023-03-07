import os

import constants
from plugin.APKPlugin import APKPlugin
from plugin.ZipPlugin import ZipPlugin

if __name__ == '__main__':
    pro_vestapk = os.path.join(constants.path_self, "pro_vestapk")
    apk = os.path.join(pro_vestapk, "tmp.apk")
    apk_obfuse = os.path.join(pro_vestapk, "ivgp_out.apk")

    # apktool
    # APKPlugin.unzip_andresguard_apk_file(apk, apk.replace(".apk", "_apktool"))
    # APKPlugin.unzip_apk_file(apk, apk.replace(".apk", "_apktool"))
    APKPlugin.unzip_apk_file(apk_obfuse, apk_obfuse.replace(".apk", "_apktool"))

    # zip
    # ZipPlugin.un_zip_file(apk, apk.replace(".apk", "_zip"))
    # ZipPlugin.un_zip_file(apk_obfuse, apk_obfuse.replace(".apk", "_zip"))

    # APKPlugin.zip_apk_file(apk_obfuse.replace('.apk', '_zip'), apk_obfuse.replace('.apk', '_new.apk'))
    # APKPlugin.zip_apk_file(apk.replace('.apk', '_apktool'), apk.replace('.apk', '_new.apk'))
    # APKPlugin.zip_andresguard_apk_file(apk.replace('.apk','_apktool'),apk.replace('.apk','_new.apk'))
