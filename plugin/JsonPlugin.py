import json


class JsonPlugin:
    @staticmethod
    def read_value_from_json_file(key, json_file):
        try:
            json_dict = json.load(open(json_file, "r", encoding="UTF-8"))
        except Exception as e:
            print(key + "读取失败")
            return ""
        return json_dict[key]

    @staticmethod
    def read_value_from_json_string(key, json_content):
        try:
            json_dict = json.loads(json_content)
        except Exception as e:
            print(key + "读取失败")
            return ""
        return json_dict[key]
