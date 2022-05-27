# coding=utf-8

from pynput import keyboard
from pynput.keyboard import Key


def on_press(key):
    """定义按下时候的响应，参数传入key"""
    try:
        print(f'输入了可打印字母: {key.char}')
    except AttributeError:
        print(f'按键不可打印，直接输出key: {key}')


def on_release(key):
    """定义释放时候的响应"""
    print(f'{key}被释放')
    if key == Key.enter:
        print(">>>>>>>>>>>>>>>>>>1")
        return False


# 监听要创建Listener，这个Listener本身就是一个threading.Thread类
# 监听写法1
def listen_1():
    with keyboard.Listener(
            on_press=on_press, on_release=on_release) as listener:
        listener.join()  # 加入线程池
        print(">>>>>>>>>>>>>>>>>>2")


# 监听写法2
def listen_2():
    listener = keyboard.Listener(
        on_press=on_press, on_release=on_release
    )
    listener.start()  # 启动线程
    listener.join()  # 加入线程池


if __name__ == '__main__':
    listen_1()