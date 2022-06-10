# 装饰器示例
import time


def deco(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("开始执行方法 >>> " + str(func))
        func(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print("time is %d ms" % msecs)

    return wrapper


@deco
def func1():
    print("这是方法1")
    time.sleep(2)


@deco
def func2():
    print("这是方法2")
    time.sleep(3)


func1()
func2()
