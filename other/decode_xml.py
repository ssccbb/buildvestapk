import os

import constants
from plugin.APKPlugin import APKPlugin

src_file = os.path.join(constants.path_self, "pro_yrjiagu/temp/AndroidManifest.xml")
encode_file = src_file.replace(".xml", "") + "_encode.xml"
decode_file = src_file.replace(".xml", "") + "_decode.xml"
APKPlugin.decode_amxl(src_file, decode_file)
# APKPlugin.encode_amxl(src_file, encode_file)
