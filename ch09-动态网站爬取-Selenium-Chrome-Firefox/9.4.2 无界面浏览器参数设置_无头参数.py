# 通过WebDriver操作进行查找，输出页面

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def main():
    # 设置为无头浏览器，即不打开浏览器，都在后台操作
    options = Options()
    options.add_argument('-headless')
    # 创建一个无头浏览器实例
    driver = webdriver.Firefox(options=options)
    # 浏览器请求网页
    driver.get("https://www.baidu.com")
    # 返回网页整个html内容
    print(driver.page_source)
    # 关闭浏览器
    driver.close()


if __name__ == '__main__':
    main()