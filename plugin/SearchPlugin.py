import os


class FileFinder:

    @staticmethod
    def find_file_in_dir(source_dir, file_end_name):
        """
        在目标文件夹内查找指定后缀名文件(逐级文件夹查找)
        :param source_dir:
        :param file_end_name:
        :return:
        """
        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            return None
        file_list = []
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                if file_name.endswith(file_end_name):
                    file_list.append(file_name)
        return file_list

    @staticmethod
    def find_file_in_cdir(source_dir, file_end_name):
        """
        在目标文件夹内查找指定后缀名文件(单级文件夹查找)
        :param source_dir:
        :param file_end_name:
        :return:
        """
        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            return None
        file_list = []
        for file_name in os.listdir(source_dir):
            if file_name.endswith(file_end_name):
                file_list.append(file_name)
        return file_list
