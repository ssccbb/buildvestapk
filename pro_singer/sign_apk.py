import os
import sys

import constants
from plugin.APKPlugin import APKPlugin
from plugin.SearchPlugin import FileFinder
from plugin.FilePlugin import FilePlugin

if __name__ == '__main__':
    path_project = os.path.join(constants.path_self, "pro_singer")
    os.chdir(path_project)
    apk_files = FileFinder.find_file_in_dir(path_project, ".apk")
    jks_files = FileFinder.find_file_in_dir(path_project, ".jks")

    if len(jks_files) != 1:
        print("请保证路径内有且仅有单个JKS文件!")
        sys.exit(0)
    jks_file = jks_files[0]
    print(f'查询到可用的JKS >>> {jks_file}')
    jks_pass = "LS880617\!@#"
    sign_content = f'-alias yr -pswd {jks_pass} -aliaspswd {jks_pass}'

    for apk_file in apk_files:
        print(f'查询到需要签名的APK >>> {apk_file}')
        APKPlugin.signer_apk_file(jks_file, sign_content, apk_file)
        FilePlugin.remove_path_file(apk_file)
    pass
