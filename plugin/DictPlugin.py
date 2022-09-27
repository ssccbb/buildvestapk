import random
import string


class DictPlugin:

    @staticmethod
    def change_str_to_dict(text):
        try:
            dict_data = eval(text)
        except Exception as e:
            print(e)
            dict_data = {}
        return dict_data

    @staticmethod
    def change_dict_to_str(dict):
        return str(dict)

    # 修改带回车的多行文本为字典集合
    @staticmethod
    def change_multi_str_to_dict(multi_str):
        dict_data = {}
        item_list = multi_str.split("\n")
        for item in item_list:
            if len(item) > 0:
                try:
                    dict_item = eval(item)
                    dict_data.update(dict_item)
                except Exception as e:
                    print(e)
        return dict_data

    @staticmethod
    def random_string(count):
        """
        生成*个随机不重复的字符串
        :return:
        """
        new_list = []
        while 1:
            value = ''.join(random.sample(string.ascii_lowercase, 6))
            if value not in new_list:
                new_list.append(value)
                if len(new_list) == count:
                    break
            else:
                continue
        return new_list

    @staticmethod
    def random_string_full(length):
        return ''.join(random.sample(string.ascii_letters + string.digits, length))
