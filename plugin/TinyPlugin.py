import os
import tinify


class TinyPlugin:

    @staticmethod
    def compress_pic_file(path):
        TinyPlugin.check_path(path)
        pass

    @staticmethod
    def compress_pic_dir(dirs):
        TinyPlugin.check_path(dirs)
        pass

    @staticmethod
    def get_file_dir(file):
        """获取文件目录通用函数"""
        fullpath = os.path.abspath(os.path.realpath(file))
        return os.path.dirname(fullpath)

    @staticmethod
    def check_suffix(file_path):
        """检查指定文件的后缀是否符合要求"""
        file_path_lower = file_path.lower()
        return (file_path_lower.endswith('.png')
                or file_path_lower.endswith('.jpg')
                or file_path_lower.endswith('.jpeg'))

    @staticmethod
    def compress_by_tinypng(input_file):
        """使用 tinypng 进行压缩，中文前面的 u 是为了兼容 py2.7"""
        if not TinyPlugin.check_suffix(input_file):
            print(u'只支持png\\jpg\\jepg格式文件：' + input_file)
            return False
        file_name = os.path.basename(input_file)
        output_path = os.path.join(TinyPlugin.get_file_dir(input_file), 'tinypng')
        output_file = os.path.join(output_path, file_name)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        try:
            source = tinify.from_file(input_file)
            source.to_file(output_file)
            print(u'文件压缩成功：' + input_file)
            old_size = os.path.getsize(input_file)
            print(u'压缩前文件大小：%d 字节' % old_size)
            new_size = os.path.getsize(output_file)
            print(u'文件保存地址：%s' % output_file)
            print(u'压缩后文件大小：%d 字节' % new_size)
            print(u'压缩比： %d%%' % ((old_size - new_size) * 100 / old_size))
        except tinify.errors.AccountError:
            print(u'使用量已超，请更新 Key')
            return True
        return False

    @staticmethod
    def check_path(input_path):
        """如果输入的是文件则直接压缩，如果是文件夹则先遍历"""
        keys = [
            'GBvFb75Gm3JQ5Dyfp13m19z1536Tv3Dq',
            'bl5YwlVryNZjbsXSzvn6Yms7BH9GYTmP',
            'DygR3gZq78FzkFdFH9Ny3nsmHz37YY7R'
        ]
        if os.path.isfile(input_path):
            while TinyPlugin.compress_by_tinypng(input_path):
                keys.remove(keys[0])
                if len(keys) == 0:
                    print(f'暂无可用key')
                    return
                tinify.key = keys[0]
        elif os.path.isdir(input_path):
            dirlist = os.walk(input_path)
            for root, dirs, files in dirlist:
                for filename in files:
                    pic = os.path.join(root, filename)
                    while TinyPlugin.compress_by_tinypng(pic):
                        keys.remove(keys[0])
                        if len(keys) == 0:
                            print(f'暂无可用key')
                            return
                        tinify.key = keys[0]
        else:
            print(u'目标文件(夹)不存在，请确认后重试。')
