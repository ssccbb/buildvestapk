from pro_codeanalysis.Regular import *
from plugin.FilePlugin import *
import re
import time


def deco(func):
    """
    装饰器打印方法耗时
    :param func: 执行的方法
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(("开始执行 >>> %s" % str(func)).join(("\033[7m", "\033[0m")))
        func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print(("执行方法%s耗时 >>> %d ms" % (str(func), msecs)).join(("\033[7m", "\033[0m")))

    return wrapper


@deco
def test():
    path = "/Users/sung/sung/pycharm-projects/buildvestapk/other/text.java"
    count = 0
    content = FilePlugin.read_str_from_file(path)
    while count < 3:
        result = re.search(Regular.r_method(), content, re.M)
        print(f'count={count},log={result.group().strip()}')
        count += 1


if __name__ == '__main__':
    test()
