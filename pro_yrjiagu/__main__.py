import os
import sys

import constants
import pro_yrjiagu.CacheUtil
from pro_yrjiagu.process import JGApplication
from plugin.SearchPlugin import FileFinder

if __name__ == '__main__':
    cache_util = pro_yrjiagu.CacheUtil.CacheUtil("jiagu_apk_info", "jiagu.ini")
    path_project = os.path.join(constants.path_self, "pro_yrjiagu")
    find_apks = FileFinder.find_file_in_dir(path_project, "release.apk")
    find_jkss = FileFinder.find_file_in_dir(path_project, ".jks")
    if len(find_jkss) != 1:
        print("请确认路径内仅有一个jks文件！")
        sys.exit(0)
    if len(find_apks) != 1:
        print("请确认路径内仅有一个apk文件！")
        sys.exit(0)
    apk_file_name = find_apks[0]
    signature_file = find_jkss[0]
    signature_content = cache_util.read_value_from_cache("signature_content")
    android_sdk_path = cache_util.read_value_from_cache("android_sdk_path", constants.path_android_sdk)
    gradle_path = cache_util.read_value_from_cache("gradle_path", "gradle")
    print("1.请确认配置了 jdk环境变量")
    print("2.请确认文件路径 没有中文")
    print(f"3.当前配置的apk文件为 {apk_file_name}")
    print(f"4.当前配置的签名文件为 {signature_file}")
    print(f"4.当前配置的签名信息为 {signature_content}")
    print(f"6.当前电脑配置的android_sdk路径为 {android_sdk_path}")
    print(f"7.当前电脑配置的gradle_path路径为 {gradle_path}")
    print("8.请确认apk文件已做raw资源引用处理")
    input("输入任意内容以便开始任务")
    jgApp = JGApplication(signer_file=signature_file, signer_content=signature_content)
    # jgApp.create_jiagu_apk(apk_file_name=apk_file_name)
    jgApp.create_jiagu_apk_by_hook_application(apk_file_name=apk_file_name,
                                               android_sdk_path=android_sdk_path
                                               , gradle_path=gradle_path)
