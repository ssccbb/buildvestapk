import os

import constants
from plugin.ZipPlugin import ZipPlugin
from plugin.AESPlugin import AESPlugin

out_put_file = os.path.join(constants.path_self, "pro_yrjiagu/temp_xed")
aesPlugin = AESPlugin("1234567890123456", "1234567890123456")
aesPlugin.decrypt_byte_by_java(os.path.join(out_put_file, "class_dexs.piz"),
                               os.path.join(out_put_file, "class_dexs.zip"))
ZipPlugin.un_zip_file(os.path.join(out_put_file, "class_dexs_decrypt.zip"), out_put_file)
