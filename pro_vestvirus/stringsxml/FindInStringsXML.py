import os
import re
from xml.etree import ElementTree

import constants
from plugin.FilePlugin import FilePlugin


class Finder:

    def __init__(self, path_android):
        self.path_android = path_android

    def load_module(self, path_module):
        """
        加载每个strings.xml在的module下的所有可编辑文件
        :param path_module:
        :return:
        """
        # strings.xml
        strings_xml = os.path.join(path_module, 'src/main/res/values/strings.xml')
        if not os.path.exists(strings_xml):
            return []
        # 预加载文件
        total_paths = [
            os.path.join(path_module, 'src/main/java'),
            os.path.join(path_module, 'src/main/res'),
            os.path.join(path_module, 'src/main/res-umc')
        ]
        # 所有可编辑文件路径
        total_files = []
        for total_path in total_paths:
            if not os.path.exists(total_path):
                continue
            for root, dirs, files in os.walk(total_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not os.path.exists(file_path):
                        continue
                    if FilePlugin.is_text_file(file_path):
                        total_files.append(file_path)
        return total_files


    def load_file(self, path_file):
        """
        加载文件内引用的字符串（可编辑文件都统计）
        :param path_file:
        :return:
        """
        total_matchs = []
        regular_java = f'R\\.string\\.[\\w_]+'
        regular_xml = f'@string/[\\w_]+'
        file_content = FilePlugin.read_str_from_file(path_file)
        # 找java的引用
        for result in re.compile(regular_java, re.M).finditer(file_content):
            if result is None:
                continue
            result = result.group().lstrip().strip()
            if result in total_matchs:
                continue
            else:
                total_matchs.append(result)
        # 找xml的引用
        for result in re.compile(regular_xml, re.M).finditer(file_content):
            if result is None:
                continue
            result = result.group().lstrip().strip()
            if result in total_matchs:
                continue
            else:
                total_matchs.append(result)
        return total_matchs
    
    
    def deal_strings_xml(self):
        """
        处理strings.xml定义字符串的引用
        :return:
        """
        # 预加载文件 [{strings.xml路径 : [该module下所有的可编辑文件路径]}]
        module_list = {
            os.path.join(self.path_android, "app/src/main/res/values/strings.xml"): self.load_module(os.path.join(self.path_android, "app")),
            os.path.join(self.path_android, "library-beauty/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "library-beauty")),
            os.path.join(self.path_android, "library-commonlib/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "library-commonlib")),
            os.path.join(self.path_android, "library-eventbus/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "library-eventbus")),
            os.path.join(self.path_android, "library-im/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "library-im")),
            os.path.join(self.path_android, "module-community/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-community")),
            os.path.join(self.path_android, "module-ext/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-ext")),
            os.path.join(self.path_android, "module-live/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-live")),
            os.path.join(self.path_android, "module-message/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-message")),
            os.path.join(self.path_android, "module-party/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-party")),
            os.path.join(self.path_android, "module-vchat/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "module-vchat")),
            os.path.join(self.path_android, "YR-Network/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "YR-Network")),
            os.path.join(self.path_android, "YR-Player/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "YR-Player")),
            os.path.join(self.path_android, "YR-SvgaImage/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "YR-SvgaImage")),
            os.path.join(self.path_android, "YR-Tools/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "YR-Tools")),
            os.path.join(self.path_android, "YR-Uikit/src/main/res/values/strings.xml"): self.load_module(
                os.path.join(self.path_android, "YR-Uikit"))
        }
        # 预加载出现的字符串 {可编辑文件路径 ： [所有引用到的字符串id]}
        use_list = {}
        for module_keys in module_list.keys():
            for file_path in module_list.get(module_keys):
                use_list.update({file_path: self.load_file(file_path)})
        # 挨个查找strings.xml内定义的字符串有无使用
        for path_xml in module_list.keys():
            if not os.path.exists(path_xml) or module_list.get(path_xml) is None or len(module_list.get(path_xml)) == 0:
                continue
            print(f'======={path_xml}')
            root = ElementTree.parse(path_xml).getroot()
            total_element = root.findall('string')
            if total_element is None or len(total_element) == 0:
                continue
            # 获取所有的string-name
            for element in total_element:
                name = element.attrib.get("name")
                if re.match(name, 'app_name') or re.match(name, 'app_name_alias'):
                    continue
                has_use = False
                # 该module下所有的可编辑文件
                path_files = module_list.get(path_xml)
                for file in path_files:
                    # 该文件所有的字符串引用
                    total_strings = use_list.get(file)
                    # print(f'{file} ===== {total_strings}')
                    if total_strings is not None and (
                            f'R.string.{name}' in total_strings or f'@string/{name}' in total_strings):
                        has_use = True
                        print(f'{name} has used in {file}')
                # print(f'{name} has use ? {has_use}')
                # 移除无用的element
                if not has_use:
                    root.remove(element)
            if os.access(path_xml, os.F_OK):
                os.remove(path_xml)
                new_tree = ElementTree.ElementTree(root)
                new_tree.write(path_xml, encoding='utf-8')
        pass
    
    
    def deal_encrypt_string(self):
        # gradle
        # UseForBaodu.java
        pass
