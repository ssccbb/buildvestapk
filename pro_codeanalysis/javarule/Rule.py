# coding=utf-8
import re
import sys
import time
from pro_codeanalysis.Regular import *


def deco(func):
    """
    装饰器打印方法耗时
    :param func: 执行的方法
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(("开始执行 >>> %s" % str(func)).join(("\033[7m", "\033[0m")))
        result = func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print(("执行方法%s耗时 >>> %d ms" % (str(func), msecs)).join(("\033[7m", "\033[0m")))
        return result

    return wrapper


class Code:

    def __init__(self, content):
        self.content = content
        self.part_of_code = []

    @staticmethod
    def code_part_by_dicts(dict_starts, dict_ends):
        """
        拆分代码片段
        :param dict_starts: 所有{出现的position
        :param dict_ends: 所有}出现的position
        :return: 代码片段 [(0,2),(2-4)]
        """
        if len(dict_starts) == 0 or len(dict_ends) == 0:
            return []
        # 代码段集合
        dicts = []
        # 排序过的所有位置
        dicts_all = sorted(dict_starts + dict_ends)
        for start_pos in dict_starts:
            # start_pos 下标
            all_pos_start = dicts_all.index(start_pos)
            for end_pos in dict_ends:
                # } 必须在 { 之后
                if end_pos < start_pos:
                    continue
                # end_pos 下标
                all_pos_end = dicts_all.index(end_pos)
                # start_pos 与 end_pos 中间的大括号（不区分左右）
                dicts_interval = dicts_all[all_pos_start + 1:all_pos_end]
                # 中间区域有多少个 {
                len_starts = len(set(dicts_interval) & set(dict_starts))
                # 中间区域有多少个 }
                len_ends = len(set(dicts_interval) & set(dict_ends))
                # 配对大括号
                if len_starts == len_ends:
                    dicts.append((start_pos, end_pos))
                    break
        return dicts

    def code_part_by_string(self):
        # {}都是成对出现
        re.purge()
        code_part_starts = [m.start() for m in re.compile('{').finditer(self.content)]
        code_part_ends = [m.start() for m in re.compile('}').finditer(self.content)]
        # java代码规范
        if len(code_part_starts) == len(code_part_ends) and len(code_part_starts) >= 0:
            # print(f'段落括号出现的次数={len(code_part_starts)}, {len(code_part_ends)}')
            self.part_of_code = Code.code_part_by_dicts(code_part_starts, code_part_ends)
            return self.part_of_code
        else:
            raise Exception("Java书写格式不规范")
            sys.exit(0)

    def code_match_package(self):
        re.purge()
        result = re.compile(Regular.r_head_package(), re.M).search(self.content)
        if result is not None:
            return result.group().strip().replace("package", "").lstrip().replace(";", "").strip()
        return None

    def code_match_import(self):
        re.purge()
        result = re.finditer(Regular.r_import(), self.content)
        if result is not None:
            import_dict = []
            for group in result:
                import_dict.append(group.group().strip().replace("import", "").lstrip().replace(";", "").strip())
        return import_dict if import_dict is not None else None

    def code_match(self, position):
        print(f'解析第{position}个代码块')
        if self.part_of_code is None or position < 0 or position >= len(self.part_of_code):
            raise Exception("超出可处理范围")
            sys.exit(0)
        start_position = 0
        if position > 0:
            start_position = self.part_of_code[position - 1][0]
        end_position = self.part_of_code[position][0] + 1
        wait_match_content = self.content[start_position:end_position]

        splits = wait_match_content.split('\n')
        # 方法|类一般是另起一行 为了减少正则匹配的复杂度 只取和{临近的一行
        if len(splits) > 1 and splits[len(splits) - 1].lstrip().startswith('{'):
            return splits[len(splits) - 2] + splits[len(splits) - 1]
        return splits[len(splits) - 1]

    def code_match_class(self, match_content):
        class_dict = {}
        # print(f'等待匹配的字符串---->{match_content}')
        re.purge()
        class_match = re.compile(Regular.r_class(), re.M).search(match_content)
        if class_match is not None:
            result = class_match.group().strip()
            # 分段代码起始位置
            class_dict.update({"start_pos": self.content.index(result)})
            # 类名以及类型
            class_dict.update({"type": Classes.get_class_type(result)})
            class_dict.update({"name": Classes.get_class_name(result)})
            # 访问权限
            class_dict.update({"permission": Classes.get_class_permission(result)})
            # 修饰符
            class_dict.update({"modifier": Classes.get_class_modifier(result)})
            # 父类
            class_dict.update({"parent": Classes.get_class_parent(result)})
            # 实现
            class_dict.update({"implements": Classes.get_class_implement(result)})
            print(f'匹配到类{class_dict}')
        return class_dict

    def code_match_method(self, match_content):
        method_dict = {}
        # print(f'等待匹配的字符串---->{match_content}')
        result = None
        # 静态代码块比较靠前优先匹配静态代码块
        re.purge()
        method_match_init_static = re.compile(Regular.r_method_initialize_static(), re.M).search(match_content)
        if method_match_init_static is not None:
            result = method_match_init_static.group().strip()
            method_dict.update({"type": "static"})
        else:
            # 接下来靠前的是初始化代码
            re.purge()
            method_match_init = re.compile(Regular.r_method_initialize(), re.M).search(match_content)
            if method_match_init is not None:
                result = method_match_init.group().strip()
                method_dict.update({"type": "initialize"})
            else:
                # 最后是正常的方法
                re.purge()
                method_match = re.compile(Regular.r_method(), re.M).search(match_content)
                if method_match is not None:
                    result = method_match.group().strip()
                    method_dict.update({"type": "normal"})
        if result is not None:
            # 匹配的结果需要先去掉头部空格 不然会影响代码区域计算
            result.lstrip()
            # 分段代码起始位置
            method_dict.update({"start_pos": self.content.index(result)})
            # 方法名
            method_dict.update({"name": Method.get_method_name(result)})
            # 访问权限
            method_dict.update({"permission": Method.get_method_permission(result)})
            # 修饰符
            method_dict.update({"modifier": Method.get_method_modifier(result)})
            # 返回类型
            method_dict.update({"return_type": Method.get_method_return(result)})
            # 方法参数
            method_dict.update({"param": Method.get_method_params(result)})
            print(f'匹配到方法{method_dict}')
        return method_dict

    def code_match_var(self):
        self.content
        return []


class Method:

    @staticmethod
    def get_method_name(content):
        re.purge()
        result = re.compile(Regular.r_method_name()).search(content)
        return result.group().strip().replace("(", "").lstrip()

    @staticmethod
    def get_method_params(content):
        times = content.count("(")
        if times != 1:
            raise Exception(f'{content}---->不符合方法规范')
        params = []
        re.purge()
        for param in re.compile(Regular.r_method_params()).finditer(content[content.find("("):len(content)]):
            params.append(param.group().strip())
        return params if params is not None else None

    @staticmethod
    def get_method_modifier(content):
        params = []
        re.purge()
        content = content.split('(')[0]
        for modifier in re.compile(Regular.r_modifier().replace('*', '{1}')).finditer(content):
            params.append(modifier.group().strip())
        return params if params is not None else None

    @staticmethod
    def get_method_return(content):
        re.purge()
        result = re.compile(Regular.r_method_return()).search(content)
        return result.group().strip().split(" ")[0]

    @staticmethod
    def get_method_permission(content):
        regular = '^' + Regular.r_permission()
        re.purge()
        result = re.compile(regular).search(content)
        if result is not None:
            return result.group().strip()
        return None


class Classes:

    @staticmethod
    def get_class_name(content):
        re.purge()
        regular = '^' + Regular.r_permission() + '\\s*' + Regular.r_modifier() + '\\s*' + Regular.r_class_type() + '{1}\\s*'
        result = re.compile(regular, re.M).search(content)
        if result is not None:
            content = content.replace(result.group(), "")
            regular = '^' + Regular.r_name()
            re.purge()
            clz_name = re.compile(regular, re.M).search(content)
            if clz_name is not None:
                return clz_name.group().strip()
        return None

    @staticmethod
    def get_class_permission(content):
        regular = '^' + Regular.r_permission()
        re.purge()
        result = re.compile(regular, re.M).search(content)
        if result is not None:
            return result.group().strip()
        return None

    @staticmethod
    def get_class_parent(content):
        regular = '(extends)\\s+' + Regular.r_name() + Regular.r_t() + '?'
        re.purge()
        result = re.compile(regular, re.M).search(content)
        if result is not None:
            return result.group().strip().replace("extends", "").lstrip()
        return None

    @staticmethod
    def get_class_implement(content):
        re.purge()
        result = re.compile(Regular.r_implements(), re.M).search(content)
        if result is not None:
            return result.group().strip().replace("implements", "").lstrip().split(",")
        return None

    @staticmethod
    def get_class_methods(content):
        return None

    @staticmethod
    def get_class_vars(content):
        return None

    @staticmethod
    def get_class_modifier(content):
        re.purge()
        result = re.compile(Regular.r_modifier(), re.M).search(content)
        if result is not None:
            return [result.group().strip()]
        return None

    @staticmethod
    def get_class_type(content):
        result = re.compile(Regular.r_class_type(), re.M).search(content)
        if result is not None:
            return result.group().strip()
        return None
