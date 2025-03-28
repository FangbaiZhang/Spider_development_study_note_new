# 多个装饰器
# 装饰器函数运行顺序：
# 最靠近原始函数的装饰器@deco_1首先运行——然后运行靠近该装饰器的第二个装饰器@deco_2
# 依次启动完所有的装饰器，运行完所有装饰器中的外函数，然后启动主程序，内函数从外层向里层运行
# 注意，如果装饰器中内函数前面没有外函数，还是先运行所有的装饰器，然后运行原始函数，

import time

# 定义第一个装饰函数，函数的参数是一个函数
def deco_1(func):
    # print()是装饰器包裹函数(内部函数)之前的函数，可以称为外函数
    print("001这个是第一个装饰器的外函数(最靠近原始函数，最先运行)：")
    # 定义一个内部函数，实现具体的功能，
    # 原始函数带有不定参数，该处传入不定参数到该内部函数
    def wrapper(*args, **kwargs):
        print("第一个装饰器包裹函数(内函数)运行开始")
        func(*args, **kwargs)
        print("第一个装饰器运行结束")

    # 装饰函数的返回值是内部函数的执行结果
    return wrapper

# 定义第二个装饰器
def deco_2(func):
    print("002这个是第二个装饰器的外函数(第二个装饰器紧跟着第一个装饰器之后运行)：")
    # 定义一个内部函数，实现具体的功能，
    # 原始函数带有不定参数，该处传入不定参数到该内部函数
    def wrapper(*args, **kwargs):
        print("第二个装饰器包裹函数(内函数)运行开始")
        func(*args, **kwargs)
        print("第二个装饰器运行结束")

    # 装饰函数的返回值是内部函数的执行结果
    return wrapper

def deco_3(func):
    print("003这个是第三个装饰器的外函数(第三个装饰器紧跟着第二个装饰器之后运行)：")
    def wrapper(*args, **kwargs):
        print("第三个装饰器包裹函数(内函数)运行开始")
        func(*args, **kwargs)
        print("第三个装饰器运行结束")

    # 装饰函数的返回值是内部函数的执行结果
    return wrapper

# 使用@符号拓展函数功能，func_a就具有了deco函数的功能
@deco_3
@deco_2
@deco_1
def func_a(a, b):
    print("004原始函数开始运行(装饰器内函数已经全部开始运行)：")
    time.sleep(1)
    print("原始函数的参数求和结果：%d" % (a + b))
    print("-------------------------------")
    return "Hello World"


if __name__ == '__main__':
    func_a(1, 2)