# coding=utf-8
# 查找字符串
import os

import constants
from plugin.FilePlugin import FilePlugin

if __name__ == '__main__':
    print(str(FilePlugin.is_string_in_path("com.yr.network", os.path.join(constants.path_android_code, "com/yr/network"))))
