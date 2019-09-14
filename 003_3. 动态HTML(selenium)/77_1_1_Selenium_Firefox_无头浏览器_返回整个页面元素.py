# 通过WebDriver操作进行查找，输出页面

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def main():
    # 设置无头参数
    options = Options()
    options.add_argument('-headless')
    # 创建浏览器实例
    driver = webdriver.Firefox(options=options)
    # 请求网页
    driver.get("https://www.baidu.com")
    # 返回整个页面元素
    # 注意driver就是一个浏览器，请求页面上的静态动态内容都会显示出来
    # 因此，page_source返回的是整个页面的elements，即开发工具看到的elements
    # 动态请求源码没有，但是elements会有页面所有内容
    # 因此可以使用xpath进行定位查找，对于动态请求页面
    print(driver.page_source)
    driver.close()


if __name__ == '__main__':
    main()

