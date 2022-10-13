import os
import constants
from pro_vestvirus.Process import Process

process = Process(os.path.join(constants.path_root, "flutter-project/huajian-android"))
# 移除无用string
process.remove_unuse_strings_in_xml()
# 垃圾代码
process.build_junk_code_with_gradle()
# 替换同一张图片
# process.rewrite_pic_to_same()
# 重写用到的加密后字符串
process.rewrite_encrypt_string()
# 重写stringfog密钥
process.rewrite_string_fog()
# 更改可编辑文件md5
process.change_file_md5()




