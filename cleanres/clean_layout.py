# coding=utf-8
import os
from pathlib2 import Path

# 剔除Android项目中无用的布局资源

_root = "/Users/sung/sung/flutter-project/huajian-android/app/src/main"
_layout = "/res/layout"
# print(os.listdir(_root + _code))
# 被查文件
_source_file = []
# 目标文件
_layout_file = []
# 无使用文件
_unuse_layout = []


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
            _source_file.append(path)
            # print "is code file"
            # print "open code:" + simple_name
    pass


open_dir(_root)
print("find source file count ---- " + str(len(_source_file)))
for layout_file in os.listdir(_root + _layout):
    # print str(layout_file)
    sub_file = Path(_root + _layout + "/" + str(layout_file))
    if not sub_file.is_dir():
        _layout_file.append(_root + _layout + "/" + layout_file)
print("find layout file count ---- " + str(len(_layout_file)))


def find_keyword(path, keyword):
    file_content = open(path, "r").readlines()
    for line in file_content:
        if line.count(keyword) > 0:
            return True
    return False


for temp in _layout_file:
    print("finding....(" + str(_layout_file.index(temp)) + "|" + str(len(_layout_file)) + ")")
    file_name = str(temp).split("/")
    simple_file_name = file_name[len(file_name) - 1]
    arr = str(simple_file_name).split(".")
    keyword = arr[0]
    used_flag = False
    for target_file in _source_file:
        if find_keyword(target_file, keyword):
            used_flag = True
    # print str(temp) + " ======== " + str(used_flag)
    if not used_flag:
        _unuse_layout.append(temp)
        print(str(temp))

_unuse_layout_size = 0
print("=========  this is unuse layout list  =======")
for temp in _unuse_layout:
    file_size = os.path.getsize(temp)
    _unuse_layout_size += file_size
    print(str(temp) + " --- " + str(file_size))
print("file number : " + str(len(_unuse_layout)) + " --- total size : " + str(_unuse_layout_size))
print("=========  this is unuse layout list  =======")

print("start delete unuse resouce....")
for temp in _unuse_layout:
    os.remove(temp)
print("done")
