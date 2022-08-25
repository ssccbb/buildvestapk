import os
import shutil
from binascii import a2b_hex
import hashlib


class FilePlugin:
    FILE_NAME_PATTERN = r"[\/\\\:\*\?\"\<\>\|]"

    @staticmethod
    def wirte_str_to_file(content, filename):
        """
        把字符串写入到文件中
        :param filename:
        :param content:
        :return:
        """
        # 文件夹不存在则先创建文件夹
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name) and len(dir_name) > 0:
            os.makedirs(dir_name)
        fh = open(filename, 'w', encoding='utf-8')
        fh.write(content)
        fh.close()

    @staticmethod
    def wirte_byte_to_file(byte_buff, filename):
        """
        把字符串写入到文件中
        :param filename:
        :param content:
        :return:
        """
        # 文件夹不存在则先创建文件夹
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name) and len(dir_name) > 0:
            os.makedirs(dir_name)
        with open(filename, "wb") as fh:
            fh.write(byte_buff)
        fh.close()

    @staticmethod
    def read_str_from_file(filename):
        """
        从文件中读取字符串
        :param filename:
        :param contents:
        :return:
        """
        try:
            fh = open(filename, 'r', encoding='utf-8')
            content = fh.read()
            fh.close()
        except Exception as e:
            content = ""
        return content

    @staticmethod
    def read_byte_from_file(filename):
        """
        从文件中读取byte
        :param filename:
        :param contents:
        :return:
        """
        try:
            fh = open(filename, 'rb')
            content = fh.read()
            fh.close()
        except:
            content = None
        return content

    @staticmethod
    def copy_file(srcfile, dstfile):
        """
        拷贝文件
        :param srcfile:
        :param dstfile:
        :return:
        """
        if not os.path.isfile(srcfile):
            print("%s not exit!" % (srcfile))
            return
        if dstfile.find("/") == -1:
            fpath, fname = None, dstfile
        else:
            fpath, fname = os.path.split(dstfile)
        if fpath is not None and not os.path.exists(fpath):
            os.makedirs(fpath)
            shutil.copyfile(srcfile, dstfile)
            print("目标文件已经拷贝至 " + dstfile)
        else:
            shutil.copyfile(srcfile, dstfile)
            print("目标文件已经拷贝至 " + dstfile)

    @staticmethod
    def copy_file_by_hex(srcfile, dstfile):
        """
        拷贝文件
        :param srcfile:
        :param dstfile:
        :return:
        """
        if not os.path.isfile(srcfile):
            print("%s not exit!" % (srcfile))
            return
        if dstfile.find("/") == -1:
            fpath, fname = None, dstfile
        else:
            fpath, fname = os.path.split(dstfile)
        if fpath is not None and not os.path.exists(fpath):
            os.makedirs(fpath)
        # hexdata = "0123456789ABCDEF"  # 注意：str中的十六进制码的数量必须是偶数个，否则 a2b_hex 函数运行会出错；
        # "A~F"的大小写无所谓；
        # 除了"0~9"、"A~F"外，不要包含其他字符，例如：空格、\t
        with open(srcfile, 'rb') as frb:
            with open(dstfile, "wb") as fwb:
                hexdata = frb.read().hex()
                fwb.write(a2b_hex(hexdata))  # 把16进制字符串转化为2进制
            frb.close()
            fwb.close()

    @staticmethod
    def move_file(srcfile, dstfile):
        """
        移除文件/文件夹
        :param path:
        :return:
        """
        if not os.path.isfile(srcfile):
            print("%s not exit!" % (srcfile))
            return
        if dstfile.find("/") == -1:
            fpath, fname = None, dstfile
        else:
            fpath, fname = os.path.split(dstfile)
        if fpath is not None and not os.path.exists(fpath):
            os.makedirs(fpath)
            shutil.move(srcfile, dstfile)
        else:
            shutil.move(srcfile, dstfile)

    @staticmethod
    def replace_folder_name(filePath, old_name, new_name):
        """
        替换文件夹名称
        :param filePath:
        :param old_name:
        :param new_name:
        :return:
        """
        for root, dirs, files in os.walk(filePath):
            for dir in dirs:
                old_dir = os.path.join(root, dir)  # 原来的文件路径
                # print("old_dir=" + old_dir)
                new_dir = old_dir.replace(old_name, new_name)
                # print("new_dir=" + new_dir)
                if old_dir != new_dir:
                    os.rename(old_dir, new_dir)  # 重命名

    @staticmethod
    def replace_file_content(filePath, old_name, new_name):
        """
        替换文件内容
        :param filePath:
        :param old_name:
        :param new_name:
        :return:
        """
        for root, dirs, files in os.walk(filePath):
            for file in files:
                filename = os.path.join(root, file)
                if filename.endswith('.java') or filename.endswith('.xml') or filename.endswith(
                        '.json') or filename.endswith('.pro'):
                    fileRead = open(filename, 'r', encoding='UTF-8')
                    lines = fileRead.readlines()
                    fileWrite = open(filename, 'w', encoding='UTF-8')
                    for s in lines:
                        result = s.replace(old_name, new_name)
                        # print(result)
                        fileWrite.write(result)  # replace是替换，write是写入
                    fileRead.close()
                    fileWrite.close()  # 关闭文件

    @staticmethod
    def remove_path_file(path):
        """
        移除文件/文件夹
        :param path:
        :return:
        """
        if os.path.exists(path):
            if os.path.isfile(path):
                print("删除文件 >>> " + path)
                os.remove(path)
            else:
                print("删除路径 >>> " + path)
                shutil.rmtree(path)

    @staticmethod
    def rename_path(old_path, new_path):
        """
        重命名文件夹路径（传绝对路径）
        :param old_path:
        :param new_path:
        :return:
        """
        print("执行路径重命名 " + old_path + " >>> (new)" + new_path)
        old_path_temp = old_path.split("/")
        new_path_temp = new_path.split("/")
        if len(old_path_temp) is not len(new_path_temp):
            print("层级不一致,重命名失败")
            return
        if os.path.exists(new_path):
            print("存在目标路径 >>> " + new_path)
            FilePlugin.remove_path(new_path)
        FilePlugin.mkdir(new_path)
        for root, dirs, files in os.walk(old_path):
            for file in files:
                shutil.move(old_path + "/" + file, new_path + "/" + file)
                print("重命名执行成功")
            for subdir in dirs:
                shutil.move(old_path + "/" + subdir, new_path + "/" + subdir)
                print("重命名执行成功")
        FilePlugin.remove_path(old_path)
        print("旧路径移除 " + old_path)
        pass

    @staticmethod
    def change_str_in_dir(old_str, new_str, target_dir):
        """
        在目标文件夹查找字符串并替换
        :param old_str:
        :param new_str:
        :param target_dir:
        :return:
        """
        print("执行字符串替换 " + old_str + " >>> (new)" + new_str + "  in (dir)" + target_dir)
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_name = os.path.join(root, file)
                FilePlugin.change_str_in_file(old_str, new_str, file_name)
        pass

    @staticmethod
    def change_str_in_file(old_str, new_str, target_file):
        """
        在目标文件查找字符串并替换
        :param old_str:
        :param new_str:
        :param target_file:
        :return:
        """
        if len(old_str) == 0 or len(new_str) == 0:
            return
        print("执行字符串替换 " + old_str + " >>> (new)" + new_str + "  in  (file)" + target_file)
        with open(target_file, mode='r') as f:
            read_lines = f.readlines()
            f.close()
        with open(target_file, mode='w') as f:
            for line in read_lines:
                if old_str in line:
                    line_new = line.replace(old_str, new_str)
                    f.writelines(line_new)
                    print("替换成功！")
                else:
                    f.writelines(line)
            f.close()
        pass

    @staticmethod
    def replace_file(old_file, new_file):
        """
        直接替换文件
        :param old_file:
        :param new_file:
        :return:
        """
        print("执行文件替换 " + old_file + " >>> (new)" + new_file)
        old_file_temp = old_file.split("/")
        new_file_temp = new_file.split("/")
        if old_file_temp[len(old_file_temp) - 1] != new_file_temp[len(new_file_temp) - 1]:
            print("文件名不一致无法替换源文件")
            print("failed！")
            return
        FilePlugin.remove_path_file(old_file)
        FilePlugin.copy_file(new_file, old_file)
        pass

    @staticmethod
    def mkdir(path):
        """
        创建指定的文件夹
        :param path: 文件夹路径，字符串格式
        :return: True(新建成功) or False(文件夹已存在，新建失败)
        """
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            print(path + ' 目录已存在')
            return False
        pass

    @staticmethod
    def md5(path):
        """
        获取路径文件md5
        :param path:
        :return:
        """
        if not os.path.exists(path):
            print("f not exists >>> " + path)
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
        pass

    @staticmethod
    def is_string_in_path(content, path):
        """
        递归查找当前文件夹内所有文件是否包含content字符串
        :param content:
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return False
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if FilePlugin.is_string_in_file(content, os.path.join(root, file)):
                        return True
                for sub_dir in dirs:
                    print("find in dir >>> " + os.path.join(root, sub_dir))
                    if FilePlugin.is_string_in_path(content, os.path.join(root, sub_dir)):
                        return True
        else:
            if FilePlugin.is_string_in_file(content, path):
                return True
        return False
        pass

    @staticmethod
    def is_string_in_file(content, file):
        """
        查找当前文件内是否包含content字符串
        :param content:
        :param file:
        :return:
        """
        if not os.path.exists(file) and not os.path.isfile(file):
            return False
        # 排除文件
        if not file.endswith(".java") and not file.endswith(".pro") and not file.endswith(".xml") and not file.endswith(
                ".properties") and not file.endswith(".txt") and not file.endswith(".ini") and not file.endswith(
            ".kt") and not file.endswith(".cpp") and not file.endswith(".gradle"):
            return False
        print("find in file >>> " + file)
        with open(file, mode='r') as f:
            if content in f.read():
                return True
            return False
        pass

    @staticmethod
    def remove_path(path):
        print(path)
        if not os.path.exists(path):
            return
        dirs = path.split("/")
        if os.path.isdir(path) and not os.listdir(path):
            os.rmdir(path)
        for pos in range(len(dirs) - 1, -1, -1):
            position = len(path) - len(dirs[pos]) - 1
            path = path[0:position]
            print(path)
            if len(path) != 0 and os.path.exists(path):
                if os.path.isdir(path) and not os.listdir(path):
                    os.rmdir(path)
                else:
                    return
        pass

    @staticmethod
    def reset_files_md5(path):
        """
        重置文件的md5（仅处理图片以及文档类文件）
        :param path: 根目录
        :return:
        """
        if not os.path.exists(path):
            return False
        if os.path.isdir(path):
            print(f'开始重置文件夹下各文件的md5 >> {path}')
            for root, dirs, files in os.walk(path):
                for file in files:
                    FilePlugin.reset_file_md5(os.path.join(path, file))
                for subdir in dirs:
                    FilePlugin.reset_files_md5(os.path.join(path, subdir))
        pass

    @staticmethod
    def reset_file_md5(file):
        """
        重置文件的md5（仅处理图片以及文档类文件）
        :param file: 文件，指定类型范围
        :return:
        """
        if not os.path.exists(file):
            return
        if not FilePlugin.is_text_file(file) and not FilePlugin.is_pic_file(file):
            chars = file.split(".")
            print("不支持的文件类型 >>> " + chars[len(chars) - 1])
            return
        print(f'{file}')
        print(f'原文件md5 >> {FilePlugin.md5(file)}')
        FilePlugin.append_content_into_file("\n", file)
        print(f'修改后文件md5 >> {FilePlugin.md5(file)}')
        pass

    @staticmethod
    def append_content_into_file(append_content, file_path):
        """
        往指定文件内添加内容
        :param append_content: 待添加的内容
        :param file_path: 文件路径
        :return:
        """
        newfile = open(file_path, 'a', encoding='utf-8')
        newfile.write(append_content)
        newfile.close()
        print(f'{file_path} >> has changed')
        pass

    @staticmethod
    def is_text_file(file):
        """
        是可编辑的文本文件
        :param file:
        :return:
        """
        if file.endswith(".java") \
                or file.endswith(".pro") \
                or file.endswith(".xml") \
                or file.endswith(".properties") \
                or file.endswith(".txt") \
                or file.endswith(".ini") \
                or file.endswith(".kt") \
                or file.endswith(".cpp") \
                or file.endswith(".gradle"):
            return True
        return False

    @staticmethod
    def is_pic_file(file):
        """
        是图片文件
        :param file:
        :return:
        """
        if file.endswith(".png") \
                or file.endswith(".jpg") \
                or file.endswith(".jpeg"):
            return True
        return False
