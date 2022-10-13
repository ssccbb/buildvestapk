import os
import re


class Git:

    def __init__(self, path: str):
        self.root_path = path
        print(f'Git初始化目录=====》》》{self.root_path}')
        pass

    def log_(self, count: int):
        command = f'git log -{count}'
        print(f'execute ===>>> {command}')
        os.chdir(self.root_path)
        return os.popen(command).read()

    def clean_(self):
        command = f'git clean -xdf'
        print(f'execute ===>>> {command}')
        os.chdir(self.root_path)
        os.system(command)
        pass

    def reset_(self, commit: str):
        command = f'git reset --hard {commit}'
        print(f'execute ===>>> {command}')
        os.chdir(self.root_path)
        os.system(command)
        pass

    def reset_last_(self):
        terminal_log = self.log_(3)
        if terminal_log is None or len(terminal_log) == 0:
            raise Exception("git log 命令执行无结果")
        result = re.compile(f'commit\\s+[\\w]+', re.M).finditer(terminal_log)
        if result is None:
            raise Exception("git log 找不到可回退的提交")
        for group in result:
            commit = group.group().strip().lstrip().replace('commit', '').strip().lstrip()
            self.reset_(commit)
            return
        pass

    def remove_local_change(self):
        # 回退已提交文件的修改
        self.reset_last_()
        # 清除未提交文件（未提交的空文件夹也会被删除）
        self.clean_()
        print(f'代码回退执行成功')
        pass
