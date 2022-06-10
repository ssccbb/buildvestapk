import os
import time
import constants
from lxml import etree
# 对apk进行自定义加固操作，添加代理app，加密*.dex后缀的文件
from plugin.HookModulePlugin import HookModulePlugin

from plugin.AESPlugin import AESPlugin
from plugin.FilePlugin import FilePlugin
from plugin.ZipPlugin import ZipPlugin
from plugin.APKPlugin import APKPlugin
from pro_yrjiagu.helper.Reediter import Reediter


def deco(func):
    """
    装饰器打印方法耗时
    :param func: 执行的方法
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("开始执行方法 >>> " + str(func))
        func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print(("执行方法%s耗时 >>> %d ms" % (str(func), msecs)).join(("\033[7m", "\033[0m")))

    return wrapper


class JGApplication:

    def __init__(self, signer_file, signer_content, ):
        self.signer_file = signer_file
        self.signer_content = signer_content

    @deco
    def create_jiagu_apk_by_hook_application(self, apk_file_name, android_sdk_path=None, gradle_path=None):
        """
        创建加固apk文件，会自动根据apk本身的包名动态修改壳app的包名路径，还支持修改AES加密的key,iv
        :return:
        """
        if self.__safe_check(apk_file_name, self.signer_file):
            return
        apk_dir = apk_file_name.replace(".apk", "")
        apk_file_xed_name = apk_file_name.replace(".apk", "_yrjiagu.apk")
        FilePlugin.remove_path_file(apk_dir)
        ZipPlugin.un_zip_file(apk_file_name, apk_dir)
        axml_file = f"{apk_dir}/AndroidManifest.xml"
        axml_decode_file = "AndroidManifest_decode.xml"
        # 解密axl
        APKPlugin.decode_amxl(axml_file, axml_decode_file)
        APKPlugin.encode_amxl(axml_decode_file, axml_file)
        APKPlugin.decode_amxl(axml_file, axml_decode_file)
        apk_name, apk_package, app_version_name = APKPlugin.get_apk_info(axml_decode_file)
        # 获取代理自定义代理app的相关参数
        package_middle = apk_package.split(".")[1]
        package_middle = "proxy" + package_middle
        proxy_aar_file = f"{package_middle}.aar"
        proxy_application_name = f"com.{package_middle}.core.ProxyApplication"
        # 替换axml 主要是向清单文件内写入壳application
        self.__change_apk_manifest_txt(axml_decode_file, proxy_application_name, apk_package, app_version_name)
        # 回加密清单文件 这时候axml_file获得的是添加过壳信息的清单文件 用于重压包
        APKPlugin.encode_amxl(axml_decode_file, axml_file)
        FilePlugin.remove_path_file(axml_decode_file)
        # 加密dex文件，保证这里的key,iv和hookapplication//Proxy_Core模块代码里面的key,iv一致
        # 逐一加密
        self.__encrypt_dex(apk_dir, constants.aes_key, constants.aes_iv)
        # 修改AndroidSDK路径
        FilePlugin.wirte_str_to_file('sdk.dir=' + android_sdk_path, "../pro_yrjiagu/HookApplication/local.properties")
        # 修改壳的AES配置
        Reediter.reedit_application_aes_ini(constants.aes_key, constants.aes_iv)
        # 修改壳的包名
        HookModulePlugin.change_core_app_package(HookModulePlugin.origin_name, package_middle)
        # 开始编译aar
        HookModulePlugin.make_proxy_core_app(gradle_path=gradle_path)
        HookModulePlugin.change_core_app_package(package_middle, HookModulePlugin.origin_name)
        # 移动aar
        FilePlugin.move_file("../pro_yrjiagu/HookApplication/Proxy_Core/build/outputs/aar/Proxy_Core-release.aar",
                             proxy_aar_file)
        # 解压aar拿到classes.jar文件
        ZipPlugin.un_zip_file(proxy_aar_file, "proxy_aar_temp")
        # 转dex文件
        APKPlugin.change_jar_to_dex("proxy_aar_temp/classes.jar")
        # 壳加入源apk进行打包
        FilePlugin.move_file("proxy_aar_temp/classes.dex", f"{apk_dir}/classes.dex")
        # 移除aar临时文件夹
        FilePlugin.remove_path_file("proxy_aar_temp")
        # 移除aar临时文件
        FilePlugin.remove_path_file(proxy_aar_file)
        # 重打包
        ZipPlugin.make_zip_dir(apk_dir, apk_file_xed_name)
        FilePlugin.remove_path_file(apk_dir)
        # 重新签名
        jks = os.path.join(constants.path_yrjiagu, self.signer_file)
        old_apk = os.path.join(constants.path_yrjiagu, apk_file_xed_name)
        APKPlugin.signer_apk_file(jks, self.signer_content, old_apk)
        FilePlugin.remove_path_file(apk_file_xed_name)

    @deco
    def create_jiagu_apk(self, apk_file_name):
        """
        创建加固apk文件，代理app的包名路固定为com.proxycore.core.ProxyApplication
        :return:
        """
        if self.__safe_check(apk_file_name, self.signer_file):
            return
        # apk源文件
        apk_dir = apk_file_name.replace(".apk", "")
        # apk修改 dex -> xed 文件
        apk_file_xed_name = apk_file_name.replace(".apk", "_yrjiagu.apk")
        FilePlugin.remove_path_file(apk_dir)
        # 解包源apk
        ZipPlugin.un_zip_file(apk_file_name, apk_dir)
        # 拿到安卓清单文件（密文）
        axml_file = f"{apk_dir}/AndroidManifest.xml"
        # xml解析之后的清单文（明文）
        axml_decode_file = "AndroidManifest_decode.xml"
        # 解密axl
        APKPlugin.decode_amxl(axml_file, axml_decode_file)
        APKPlugin.encode_amxl(axml_decode_file, axml_file)
        APKPlugin.decode_amxl(axml_file, axml_decode_file)
        # 获取包信息
        apk_name, apk_package, app_version_name = APKPlugin.get_apk_info(axml_decode_file)
        # 获取代理自定义代理app的相关参数
        proxy_application_name = "com.proxycore.core.ProxyApplication"
        # 替换axml
        self.__change_apk_manifest_txt(axml_decode_file, proxy_application_name, apk_package, app_version_name)
        APKPlugin.encode_amxl(axml_decode_file, axml_file)
        FilePlugin.remove_path_file(axml_decode_file)
        # 加密dex文件
        self.__encrypt_dex(apk_dir, constants.aes_key, constants.aes_iv)
        # 添加壳app
        FilePlugin.copy_file("proxy_application.dex", f"{apk_dir}/classes.dex")
        ZipPlugin.make_zip_dir(apk_dir, apk_file_xed_name)
        FilePlugin.remove_path_file(apk_dir)
        # 重新签名
        APKPlugin.signer_apk_file(self.signer_file, self.signer_content, apk_file_xed_name)
        FilePlugin.remove_path_file(apk_file_xed_name)

    @staticmethod
    def __change_apk_manifest_txt(android_manifest_file, proxy_application_name=None, apk_package=None,
                                  app_version_name=None, output_file=None):
        """
        修改manifest.xml文件中的关键字段
        :param android_manifest_file:
        :param proxy_application_name:
        :param apk_package:
        :param app_version_name:
        :param output_file:
        :return:
        """
        if output_file is None:
            output_file = android_manifest_file
        ele_root = etree.parse(android_manifest_file, etree.XMLParser(encoding="utf-8"))
        ele_application = ele_root.find("application")
        if apk_package is None or app_version_name is None or proxy_application_name is None:
            print("参数不完整")
            return
        application_name = ele_application.attrib.get("{http://schemas.android.com/apk/res/android}name")
        element_key_name = '{http://schemas.android.com/apk/res/android}name'
        element_key_value = '{http://schemas.android.com/apk/res/android}value'
        ele_application.set(element_key_name, proxy_application_name)

        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_name', element_key_value: application_name})
        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_version', element_key_value: app_version_name})
        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_package', element_key_value: apk_package})
        axml_byte_buffer = etree.tostring(ele_root, pretty_print=True, encoding="utf-8")
        FilePlugin.wirte_byte_to_file(axml_byte_buffer, output_file)

    @staticmethod
    def __encrypt_dex(path, key, key_iv):
        """
        加密dex文件为xed文件
        :param path:
        :param key:
        :param key_iv:
        :return:
        """
        aes_plugin = AESPlugin(key, key_iv)
        if os.path.isfile(path):
            if path.find(".dex") != -1:
                aes_plugin.encrypt_byte_by_jar(path, path.replace(".dex", ".xed"))
        else:
            dex_zip = os.path.join(path, "classes.zip")
            has_dex = ZipPlugin.make_zip_dir(path, dex_zip, ".dex")
            if has_dex:
                aes_plugin.encrypt_byte_by_jar(dex_zip, dex_zip.replace(".zip", ".piz"))
                os.remove(dex_zip)

    @staticmethod
    def __safe_check(apk_file, signer_file):
        if not os.path.isfile(apk_file):
            print(f"没有在当前目录找到{apk_file}文件")
            return True
        if not os.path.isfile(signer_file):
            print(f"没有在当前目录找到{signer_file}.jks签名文件")
            return True
