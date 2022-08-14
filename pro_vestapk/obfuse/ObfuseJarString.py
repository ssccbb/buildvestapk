import constants
import os
import sys
import pexpect

from plugin.APKPlugin import APKPlugin
from plugin.SearchPlugin import FileFinder

if __name__ == '__main__':
    path_project = os.path.join(constants.path_self, "pro_vestapk")
    os.chdir(path_project)
    apk_files = FileFinder.find_file_in_dir(path_project, "_release.apk")
    if len(apk_files) != 1:
        print("请保证路径内有且仅有单个APK文件!")
        sys.exit(0)
    apk = apk_files[0]
    apk_dir = apk.replace(".apk", "")
    if not os.path.exists(apk_dir):
        APKPlugin.unzip_apk_file(apk, apk_dir)
    obfuse_jar = os.path.join(path_project, "obfuseJarString.jar")
    cmd = f"java -Dfile.encoding=utf-8 -jar {obfuse_jar}"
    os.system(cmd)
    # child = pexpect.spawn(cmd, encoding="UTF-8")
    # child.expect("请输入jar包路径")
    # child.sendline(obfuse_jar)
    # child.expect("请输入加密字符串key")
    # child.sendline("123aed")
    # APKPlugin.zip_apk_file(apk_dir, apk.replace(".apk", "_obfuse.apk"))
