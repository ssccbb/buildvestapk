# coding=utf-8
import os
import subprocess
from plugin.FilePlugin import FilePlugin
from plugin.SearchPlugin import FileFinder

import constants
from pro_yrjiagu.reediter import Reediter

# os.chdir("/Users/sung/sung/flutter-project/huajian-android")
# os.system("./gradle clean assembleRelease")

# with subprocess.Popen(["./gradlew", "assembleRelease"], shell=False,
#                       cwd="/Users/sung/sung/flutter-project/huajian-android") as p:
#     print(">>>>>>>>>>>>" + str(p.wait()))


# FilePlugin.remove_path(constants.path_self + "/aaaaa/aaab/asdca")

# for file in FileFinder.find_file_in_dir(os.path.join(constants.path_self, 'pro_yrjiagu'), '.py'):
#     print(str(file))

Reediter.reedit_hook_application_aes_ini(constants.aes_key,constants.aes_iv)
