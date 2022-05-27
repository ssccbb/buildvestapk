# coding=utf-8
from plugin.JsonPlugin import JsonPlugin
from plugin.FilePlugin import FilePlugin


class PackageParser(object):
    def __init__(self, key_package, package_json_file):
        self.packages_json = FilePlugin().read_str_from_file(package_json_file)
        if key_package in self.packages_json:
            print("配置检测通过....开始解析详细配置信息")
        else:
            raise Exception("请保持配置包名信息一致！")
        self.package_info = JsonPlugin.read_value_from_json_string(key_package, self.packages_json)

    def read_value_with_key(self, key):
        return self.package_info[key]
