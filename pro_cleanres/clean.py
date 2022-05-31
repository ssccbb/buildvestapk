# coding=utf-8
import os

# 清除无用layout释放绑定的图片资源
os.system("python clean_layout.py")
# 清除无用图片
os.system("python clean_pic.py")
