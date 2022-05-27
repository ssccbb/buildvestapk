# coding=utf-8
import os
from pathlib2 import Path

# 剔除Android项目中无用的图片资源

_root = "/Users/sung/sung/flutter-project/huajian-android/app/src/main"
_code = "/java/com"
_image = "/res"
_sub_image = ["drawable", "drawable-hdpi", "drawable-xhdpi", "drawable-xxhdpi",
              "mipmap-hdpi", "mipmap-mdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi"]

# print(os.listdir(_root + _code))
# 被查文件
_code_file = []
# 目标文件
_image_file = []
# 无使用文件
_unuse_iamges = []


def open_dir(path):
    for sub_dir in os.listdir(path):
        sub_file = Path(path + "/" + sub_dir)
        sub_path = path + "/" + sub_file.name
        if sub_file.is_dir():
            open_dir(sub_path)
        else:
            open_file(sub_path)
    pass


def open_file(path):
    # print path
    _tmp_file = Path(path)
    if _tmp_file.is_dir():
        pass
    else:
        simple_name = _tmp_file.name
        if simple_name.endswith(".java") or simple_name.endswith(".xml") or simple_name.endswith(".kt"):
            _code_file.append(path)
            # print "is code file"
            # print "open code:" + simple_name
        if simple_name.endswith(".png") or simple_name.endswith("jpg") or simple_name.endswith("jpeg"):
            _image_file.append(path)
            # print "is image file"
            # print "open img:" + simple_name
    pass


# java & xml 文件路径
open_dir(_root + _code)
print("find code file count ---- " + str(len(_code_file)))
# 图片资源文件路径
# for sub_filename in _sub_image:
#     _sub_image_path = _root + _image + "/" + sub_filename
#     # print _sub_image_path
#     open_dir(_sub_image_path)
open_dir(_root + _image)
print("find image file count ---- " + str(len(_image_file)))


def find_keyword(path, keyword):
    file_content = open(path, "r").readlines()
    for line in file_content:
        if line.count(keyword) > 0:
            return True
    return False


_image_file_num = len(_image_file)
for temp in _image_file:
    print("finding....(" + str(_image_file.index(temp)) + "|" + str(_image_file_num) + ")")
    file_name = str(temp).split("/")
    simple_file_name = file_name[len(file_name) - 1]
    arr = str(simple_file_name).split(".")
    keyword = arr[0]
    # .9在使用时依然是不带".9" 不需要特殊处理
    # if simple_file_name.find(".9") != -1:
    #     # 去掉文件后缀（保留.9）
    #     keyword = simple_file_name.replace("." + arr[len(arr)], "")
    used_flag = False
    for target_file in _code_file:
        if find_keyword(target_file, keyword):
            used_flag = True
    # print str(temp) + " ======== " + str(used_flag)
    if not used_flag:
        _unuse_iamges.append(temp)

_unuse_images_size = 0
print("=========  this is unuse image list  =======")
for temp in _unuse_iamges:
    file_size = os.path.getsize(temp)
    _unuse_images_size += file_size
    print(str(temp) + " --- " + str(file_size))
print("file number : " + str(len(_unuse_iamges)) + " --- total size : " + str(_unuse_images_size))
print("=========  this is unuse image list  =======")

print("start delete unuse resouce....")
for temp in _unuse_iamges:
    os.remove(temp)
print("done")
