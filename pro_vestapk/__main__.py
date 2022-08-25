import os
import time

import constants
from pro_vestapk.helper.Process import Process


def deco(func):
    """
    装饰器打印方法耗时
    :param func: 执行的方法
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(("开始执行 >>> %s" % str(func)).join(("\033[7m", "\033[0m")))
        func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print(("执行方法%s耗时 >>> %d ms" % (str(func), msecs)).join(("\033[7m", "\033[0m")))

    return wrapper


@deco
def creat_vest_apk():
    root = os.path.join(constants.path_self, "pro_vestapk")
    base = os.path.join(root, "base")
    process = Process(os.path.join(root, "vest_config.txt"))
    # step 1 读取配置列表
    new_vest_config = process.parser_vest_list()
    if new_vest_config is None or not os.path.exists(new_vest_config):
        raise Exception("配置文件处理失败")
    # step 2 apktool解包
    apk_temp = process.decode_apk_by_apktool()
    with open(new_vest_config, mode='r') as f:
        for vest_apk_name in f.readlines():
            vest_apk_name = vest_apk_name.strip()
            print(f"开始替换新的apk名称 >>> {vest_apk_name}")
            # step 3 修改string,xml文件内的应用名
            process.replace_apk_name(vest_apk_name)
            # step 4 apktool打包
            process.build_apk_by_apktool()
            # step 5 更名apk防覆盖
            process.replace_apk_file_name(base, vest_apk_name)
        f.close()
    # step 6 遍历签名
    process.sign_apk_files(base)
    # step 7 清除temp文件
    process.clear_temp()


@deco
def creat_new_apk():
    root = os.path.join(constants.path_self, "pro_vestapk")
    process = Process(os.path.join(root, "vest_config.txt"))
    apk_temp = process.decode_apk_by_apktool()
    process.change_md5("zmpceduser_v14.3.10_2022-08-14_release")
    process.build_apk_by_apktool()


if __name__ == '__main__':
    print("1、请确保配置了vest_config.txt文件（AABBCC格式）")
    print("2、请确保base文件夹为空")
    print("3、请确保根目录有且仅有一个apk文件以及jks文件")
    creat_vest_apk()
    # creat_new_apk()
