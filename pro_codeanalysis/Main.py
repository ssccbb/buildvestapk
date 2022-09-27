import os
import sys

import constants
from plugin.FilePlugin import FilePlugin
from pro_codeanalysis.Model import *
from pro_codeanalysis.javarule.Rule import Code

if __name__ == '__main__':
    # 示例java
    path = os.path.join(constants.path_code_analysis, "AnimManager.java")
    path_json = path.replace(".java", ".json")
    file = "AnimManager"
    # 加载文件为整体字符串
    content = FilePlugin.read_str_from_file(path)
    # 去末尾空格
    content = content.rstrip()
    # class
    class_model = Class()
    code_parser = Code(content=content)
    # 分段代码位置
    part_of_code = code_parser.code_part_by_string()
    print(f'{part_of_code}')
    if part_of_code is None or len(part_of_code) <= 0:
        raise Exception("未查询到代码分段")
        sys.exit(0)
    # 获取包路径
    class_model.package = code_parser.code_match_package()
    # 获取import包
    class_model.import_lib.append(code_parser.code_match_import())
    # 获取类相关
    temp_dict = code_parser.code_match_class(code_parser.code_match(0))
    class_model.code_area = [temp_dict.get("start_pos"), part_of_code[0][1]]
    class_model.name = temp_dict.get("name")
    class_model.type = temp_dict.get("type")
    class_model.modifier.append(temp_dict.get("modifier"))
    class_model.permission = temp_dict.get("permission")
    class_model.parent = temp_dict.get("parent")
    class_model.implement.append(temp_dict.get("implements"))
    # 循环查找代码段落
    count_position = -1
    for temp_part in part_of_code:
        count_position += 1
        if count_position == 0:
            continue
        wait_match_string = code_parser.code_match(count_position)
        # 内部类
        temp_inner_dict = code_parser.code_match_class(wait_match_string)
        if temp_inner_dict is not None and len(temp_inner_dict.keys()) > 0:
            inner_class = Class()
            inner_class.package = class_model.package + '\\.' + class_model.name
            inner_class.code_area = [temp_inner_dict.get("start_pos"), part_of_code[count_position][1]]
            inner_class.name = temp_inner_dict.get("name")
            inner_class.type = temp_inner_dict.get("type")
            inner_class.modifier.append(temp_inner_dict.get("modifier"))
            inner_class.permission = temp_inner_dict.get("permission")
            inner_class.parent = temp_inner_dict.get("parent")
            inner_class.implement.append(temp_inner_dict.get("implements"))
            class_model.inner_class.append(inner_class)
        # 方法
        temp_method_dict = code_parser.code_match_method(wait_match_string)
        if temp_method_dict is not None and len(temp_method_dict.keys()) > 0:
            method = Method(temp_method_dict.get("type"), temp_method_dict.get("name"),
                            temp_method_dict.get("start_pos"), part_of_code[count_position][1])
            method.modifier.append(temp_method_dict.get("modifier"))
            method.permission = (temp_method_dict.get("permission"))
            method.return_type = temp_method_dict.get("return_type")
            method.input_param.append(temp_method_dict.get("param"))
            class_model.methods.append(method)
    print(f'{class_model}')
    # 常/变量
    # temp_var_dict = code_parser.code_match_var()
    # if temp_var_dict is not None and len(temp_var_dict.keys()) > 0:
    #     class_model.vars.append(temp_var_dict)

