# -*- coding: UTF-8 -*-
import os, shutil, config, random

_jks_file_ = config.__dir + "/jks"
_jks_info_ = "jksinfo.txt"


# 准备文件夹
def mkdirs():
    print("mkdir() excute! whithout packagename...")
    delete()
    os.mkdir(_jks_file_)
    print("path(" + _jks_file_ + ") has creat!")
    print("need jks number -- " + str(config.__jks_number) + " -- ready to create path...")
    for num in range(config.__jks_number):
        os.mkdir(_jks_file_ + "/" + str(num + 1))
    print("listdir -- " + str(os.listdir(_jks_file_)))
    pass


def mkdirs_with_package():
    print("mkdirs_with_package() excute! whith packagename...")
    _packages = random_package_list(config.__jks_number)
    delete()
    os.mkdir(_jks_file_)
    print("path(" + _jks_file_ + ") has creat!")
    print("need jks number -- " + str(config.__jks_number) + " -- ready to create path...")
    for _package in _packages:
        os.mkdir(_jks_file_ + "/" + _package)
    print("listdir -- " + str(os.listdir(_jks_file_)))
    pass


def mkdir(_name):
    _dir = config.__dir + "/" + _name
    if os.path.exists(_dir):
        for _child_file in os.listdir(_dir):
            # 删除jksinfo.txt & xxx.jks
            os.remove(_dir + "/" + _child_file)
            print("path(" + _dir + "/" + _child_file + ") already remove")
        os.rmdir(_dir)
        print("path(" + _dir + ") already remove")
    os.mkdir(_dir)
    pass


# 创建jksinfo.txt
def creat_jksinfos():
    _need_jksinfo = config.__jks_info
    if not _need_jksinfo:
        print("do not need jksinfo.txt! skip")
        pass
    for path in os.listdir(_jks_file_):
        # 不存在会自动创建
        _file = open(_jks_file_ + "/" + path + "/" + _jks_info_, "w")
        # 清空文本文件内容
        _file.truncate()
        _file.close()
        print(_file)
    pass


def creat_jksinfo(_package):
    # 不存在会自动创建
    _file = open(config.__dir + "/" + _package + "/" + _jks_info_, "w")
    # 清空文本文件内容
    _file.truncate()
    _file.close()
    print(_file)
    pass


# 递归删除文件夹
def delete():
    if os.path.exists(_jks_file_):
        # jks递归
        for _dir in os.listdir(_jks_file_):
            # 顺序递归
            for _child_file in os.listdir(_jks_file_ + "/" + _dir):
                # 删除jksinfo.txt & xxx.jks
                os.remove(_jks_file_ + "/" + _dir + "/" + _child_file)
            shutil.rmtree(_jks_file_ + "/" + _dir)
            pass
        shutil.rmtree(_jks_file_)
        print("path(" + _jks_file_ + ") already remove")
    pass


# 删除oldjks
def deleteOldJKS(_file):
    if os.path.exists(_file):
        os.remove(_file)
    pass


# 写入jksinfo
def writeJKSInfo(_jks_info, _jks_info_dir):
    print("start write file ..." + _jks_info_dir)
    if os.path.exists(_jks_info_dir):
        _jks_file = open(_jks_info_dir, "w")
        _jks_file.write(_jks_info)
        _jks_file.close()
        print("write done!")
        pass
    pass


# 随机包名
def random_package():
    _center_lenght = random.randint(4, 7)
    _end_lenght = random.randint(5, 8)

    _strlist = list(random.sample('zyxwvutsrqponmlkjihgfedcba', _center_lenght + _end_lenght))
    _strlist.insert(_center_lenght, ".")
    _full_packagename = "com." + "".join(_strlist)

    return _full_packagename


# 随机包名列表
def random_package_list(_size):
    print("need package size --> " + str(_size))
    _package_list = set()
    print("random package generating...")
    while len(_package_list) < _size:
        _new_package = random_package()
        if _new_package in _package_list:
            _new_package = random_package()
            pass
        _package_list.add(_new_package)
    print("random package generate compelete!")
    return _package_list
