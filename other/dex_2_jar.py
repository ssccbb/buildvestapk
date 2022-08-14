import os

import constants

if __name__ == '__main__':
    path = os.path.join(constants.path_self, "pro_vestapk/npswuser_v14.3.10_2022-08-11_release_zip")
    path_obfuse = os.path.join(constants.path_self, "pro_vestapk/npswuser_v14.3.10_2022-08-11_release_obfuse_zip")
    sh = os.path.join(constants.path_self, "dex2jar-2.0/d2j-dex2jar.sh")

    os.chdir(path_obfuse)
    cmd = f"sh {sh} {path_obfuse}/classes.dex"
    if os.system(cmd) == 0:
        print("成功")
    else:
        raise Exception("失败")
