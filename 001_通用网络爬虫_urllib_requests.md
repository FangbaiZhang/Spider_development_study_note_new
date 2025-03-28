# **Python实战——网络爬虫——请求网页——学习心得笔记**
  
# 1. 网络爬虫
- 爬虫定义：
    网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），
    是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。
    另外一些不常使用的名字还有蚂蚁、自动索引、模拟程序或者蠕虫。
- 两大特征
    - 按照作者的要求下载数据和内容
    - 能自动在网络上流窜
- 三大步骤
    - 下载网页
    - 提取正确的信息
    - 根据一定的规则自动跳到另外的网页执行以上两步内容
- 爬虫分类
    - 通用爬虫（搜索引擎，类似百度，搜狗）
    - 专用爬虫（聚焦爬虫）
- Python网络爬虫包介绍
    - Python3.x
        - urllib, urllib3, httplib2, requests
    - 最常用组合：
    - urllib, requests
        - urllib中的request.urlopen 请求网页
        - requests.get 请求网页
        
# 2. urllib包
## 2.1. 包含模块
- urllib.request: 打开和读取urls
- urllib.error: 包含urllib.request产生的常见错误，使用try捕捉                                  
- urllib.parse: 包含解析url的方法
- urllib.robotparse: 解析robots.txt文件

- 查看实例43_1
- 计算机内存使用的Unicode编码的字节，
- 存储显示的时候转换为UTF-8编码的字符串
- 参考我的博客对编码的解释（计算机常识栏目）
    
## 2.2. 网页编码问题的解决
- chardet 可以自动检测页面文件的编码格式，但是可能有误 
- 比如上面实例运行后结果开头里面就有：
<head>
    <meta ...... charset=UTF-8"/>    
- 需要安装chardet包
    - pycharm虚拟环境下安装包，直接进入解释器设置界面，点击包列表右边
    - 的加号，进去搜索所需的包，安装即可
    - 自动检测编码看实例
    - 43_2
	    
## 2.3. urlopen的返回对象
- rsp = request.urlopen(url)  
- 有时候不一定能获得对象，断网了，服务器故障等等
- geturl: 返回请求对象的URL
- info: 返回反馈对象的meta信息
- getcode: 返回的http code（状态码）
- 看实例43_3
    
## 2.4. request.data
- 访问网络的两种方法
    - get 
        - 利用参数给服务器传递信息
        - 参数为dict,使用parse编码
        - 看实例43_4
    - post
        - 一般向服务器传递参数使用
        - post是把信息自动加密处理
        - 我们如果想使用post信息，需要使用data参数
        - 使用post,意味着http请求头可能需要更改:
            - Content-Type: application/x-www.form-urlencode
            - Content-Length: 数据长度
            - 简而言之，一旦更改请求方法，注意其它请求头部信息相适应         
            - 看实例43_5/6
            - 为了更多的设置请求信息，单纯通过urlopen就不太适用了
            - 需要使用request.Request类 

- get与post的区别：
    POST请求的参数都在放在formdata中，可以查看有道翻译，翻译一个单词，
    检查network中headers，里面有formdata，里面有发送请求的相关参数。
    浏览器地址栏中的网址没有发生变化。可以参考有道翻译：
    http://fanyi.youdao.com/

    get请求：请求的参数直接放在url地址之中，
    请求的参数进行url编码直接放在地址中，可以参考豆瓣的电影排行榜:
    https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=
    
    具体区别：
        参考案例43_18_1为有道post请求
        43_4为get请求
        
- POST请求一般用于提交表单，传输大量的数据
- 其它请求一般都使用的GET请求


（注：判断post与get请求最显著的区别就是url地址是否发生变化，发生变化了就是get，反之则是post请求，post请求的参数是在表单里）               

## 2.5. urllib.error
- URLError产生的原因
    - 没网
    - 服务器连接失败
    - 是OSError的子类
    - 看案例43_7
- HTTPError是URLError的一个子类
    - 看案例43_8
- 两者区别：
    - HTTPError是对应的HTTP请求的返回码错误
    - 如果返回错误码是400以上的则返回HTTPError
    - URLError对应的一般是网络出现错误，包括url问题
    - 关系区别：OSError-URLError-HTTPError
- 爬虫执行以下代码时候，都放在try模块下
    try:
        req = request.Request(url)
        rsp = request.urlopen(req)  
        
## 2.6. UserAgent
- UserAgent: 用户代理，简称UA，属于headers的一部分，服务器通过UA来判断访问者的身份
- 用途：用户伪装成一个浏览器访问
- 缺点：虽然用户伪装成一个浏览器访问，但是频繁的访问还是可能会被封IP地址
- 常见的UA值，使用的时候可以直接复制粘贴，也可以用浏览器访问的时候抓包
    - 电脑端 
    chrome 
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11 
    Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16
    
    Firefox 
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0 
    Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10
                         
    - 移动端
    Android 
    Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 
    Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
    IPhone 
    Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5
    
    - 更多UA值请参考博客
    - https://blog.csdn.net/u011318077/article/details/86508095

- UserAgent的使用  
    - 看实例43_9  
    
# 3. ProxyHandler处理（代理服务器）
- 使用代理IP，是爬虫的常用手段
- 服务器有反爬虫手段，使用代理就是反反爬虫
- 获取代理服务器的地址：
    - www.xicidaili.com
    - www.goubanjia.com
- 代理用了隐藏真实的访问，代理也不允许频繁的访问某一个固定的网址，
- 所以代理IP一定要很多很多,然后更换不同的IP访问
- 基本使用步骤：
    - 设置代理地址
    - 创建ProxyHandler
    - 创建Opener
    - 安装Opener
    - 看案例43_10        
    
# 4. cookie & session
- 产生的原因：
    - 由于HTTP协议没有记忆性，人们为了弥补这个缺陷，所采用的一个补充协议
    - cookie是发放给用户（即http浏览器）的一段信息，session是保存在服务器上的
    - 对应的另一半信息，用来记录用户的信息

- cookie和session的区别
    - 存放位置不同
    - cookie不安全
    - session会保存在服务器上一段时间，有一定的期限，会过期
    - 单个cookie数据不超过4KB，很多浏览器限制一个站点最多保存20个
    
- session的存放位置
    - 存在服务器端
    - 一般情况，session是放在内存中或者数据库中

- 没有cookie登陆，模拟登陆人人网  
    - 看案例43_11 
    - 没有cookie的登陆，返回的网页为未登陆状态，自动跳转到登陆首页
    
- 使用cookie登陆人人网
    - 直接将网页中的cookie复制下来，然后手动放入请求头
    - 看案例43_12   
    
- cookie模块
    - http模块包含一些关于cookie的模块，通过他们我们可以自动使用cookie
        - CookieJar
            - 管理存储cookie，向传出的http请求头添加cookie
            - cookie存储在内存中，CookieJar实例回收后cookie将消失
        - FileCookieJar(filename, delayload=None, policy=None)
            - 使用文件管理cookie
            - filename是保存cookie的文件
        - MozillaCookieJar(filename, delayload=None, policy=None)
            - 创建与Mozilla浏览器cookie.txt兼容的FileCookie案例
        - LwpCookieJar(filename, delayload=None, policy=None)
            - 创建与libwww-perl标准兼容的Set-Cookie3格式的FileCookieJar实例
        - 他们关系是：CookieJar-->FileCookieJar-->MozillaCookieJar&LwpCookieJar
    - 利用CookieJar访问人人网
        - 看实例43_13
        - 自动使用cookie登陆的流程
            - 打开登陆页面后自动通过用户密码登陆
            - 自动提取反馈回来的cookie
            - 利用提取的cookie登陆隐私页面
        - 案例中的handler是Handler的实例，常规用法参考实例
            
                # 生成cookie的管理器
                cookie_handler = request.HTTPCookieProcessor(cookie)
                # 创建http请求管理器
                http_handler = request.HTTPHandler()
                # 生成https管理器
                https_handler = request.HTTPSHandler()
                
    - 创建handler之后，使用opener打开，打开后相应的业务由相应的handler处理
        - 将cookie作为一个变量打出来
        - 参考案例43_14 
            - cookie的属性
                - name: 名称
                - value： 值
                - domain： 可以访问此cookie的域名
                - path： 可以访问此cookie的页面路径
                - expires: 过期的时间
                - size：大小
                - http字段
                    
    - cookie的保存
        - 使用FileCookieJar 
        - 参考案例43_15
            
    - cookie的读取
        - 使用cookie.load('cookie.txt')
        
# 5. SSL数字证书
- SSL就是指遵守SSL安全套阶层协议的服务器数字证书（SecureSocketLayer)
- 理论上网址带有https:都是安全的，带有SSL数字证书 
- CA(Certificate Authority) 是数字证书认证中, 发放管理废除数字证书的第三方机构
- 遇到不信任的SSL证书，需要进行单独处理
    - 参考案例43_17 
    
# 6. js加密
- 有的反爬虫策略采用js对需要传输的数据进行加密处理（通常是取md5值）
- 经过加密，传输的就是密文，但是加密函数或者过程一定是在浏览器完成，
- 也就是一定会把代码（js代码）暴露给使用者
- 通过阅读加密算法，就可以模拟出加密的过程，从而达到破解
- 参考案例43_18未成功实现,由于存在加密，需要对加密进行破解，
- 43_18_1为修改后的实例，修改网址，删除网址中的_o
- 跳过了了JS加密程序，跳过了salt和sign
- 成功实现中英，英中翻译

- 通过破解加密过程参考6.1和案例43_19, 43_19_1

## 6.1 有道翻译js加密
- 有道翻译在线进行了加密过程，检查源码发现formdata中有salt和sign两个键
- salt(俗称加盐，一个附加的字符串，附加之后然后进行加密，
    - 类似于一般用户输入密码位数有限，服务器会给密码附加一串随机的数值，然后再进行加密，
    - 加密一般都是JS加密)
- sign(加密后的字段)

- 提取有道翻译的JS数据
    - 打开有道翻译首页，检查，刷新一下，参考图片43_19.png,然后复制里面的JS数据
    - 数据易读性很差，到在线网站http://tool.oschina.net/codeformat/js进行格式化一下
    - 将格式化的数据保存到，43_19.txt中，
    - 然后ctrl+f查找salt，会找到多个salt,找到以下salt
       
        function(e, t) {
            var n = e("./jquery-1.7");
            e("./utils");
            e("./md5");
            var r = function(e) {
                var t = n.md5(navigator.appVersion),
                r = "" + (new Date).getTime(),
                i = r + parseInt(10 * Math.random(), 10);
                return {
                    ts: r,
                    bv: t,
                    salt: i,
                    sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
                }         
        
    - 查看数据发现 i = "" + (new Date).getTime() + parseInt(10 * Math.random(), 10)
    - 上面的i就是计算salt的值的公式
    - 上面的sign中值是一个计算md5的公式
    - sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
        - md5后面的括号中为计算公式，包含以下部分
            - 第一部分和第四部分为两个字符串
            - 第三部分就是i,就是上面salt对应的值
            - 第二部分为e,是输入的一个值，经推测，应该是输入的单词
                                              
- 具体实现过程参考案例43_19, 43_19_1
- 案例43_19是按照我本地的加密算法，但是最终未成功，未找到原因，可能是JS加密数据复制过程中出现了问题 
- 案例43_19_1是群里案例成功破解的代码，过程一样，但是有道修改加密规则后会失效

# 7. ajax异步请求
- 异步请求
- 一定会有url，请求方法，可能有数据  
- 一般使用json格式
- 豆瓣排行榜-剧情：https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=
- 该网页向下拉动，一直拉不完，会自动请求，更新页面，就是使用了ajax请求
    - 打开上面网页，然后滚动，检查页面，观察每次向下滚动的变化，发现，每次向下滚动
    - 会出来一个新的请求网址，同时每次更新的图片也在20张，
    - 参考图片43_20.png
    - 拿出其中两个请求URL进行比较分析
    
    https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=20&limit=20
    https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=40&limit=20
        
        https://movie.douban.com/j/chart/top_list?
        电影类型剧情：type=11&
        评分区间好于100%到90%的影片：interval_id=100%3A90&
        这个不管：action=&
        从第四十部开始：start=40&
        每次刷新限制为20部，下面对应20张图片请求：limit=20
        
- 案例43_20,爬取豆瓣电影数据  

# 7. Requests
- HTTP for Humans-献给人类，更好用，更简洁
- 继承了urllib的所有特性
- 底层使用的是urllib3
- 开源地址：https://github.com/requests/requests
- 中文文档：http://docs.python-requests.org/zh_CN/latest/#

## 7.1. get请求
- 有两种方式
    - requests.get(url)
    - requests.request('get', url)
    - 可以带有headers和params参数
    - 参考案例43_21
    
- get返回的内容
    - 参考案例43_22   
    
## 7.2. post请求    
- rsp = requests.post(url, data=data)
- 参考案例43_23    

## 7.3. proxy代理
- proxy
    
    proxies = {
        'http': 'address of proxy',
        'https': 'address of proxy',
    }
    
    rsp = requests.request('get', 'http//:xxx')
    
- 代理有可能报错，如果使用人数多，考虑安全问题，代理可能被强行关闭

## 7.4. 用户验证
- 代理验证
    - 可能需要使用HTTP basic Auth, 类似下面
    - 格式为:用户名：密码@代理地址:端口地址
    proxy = {'http': 'name:123456@192.168.1.123:4444'}
    rsp = requests.get('http://www.baidu.com', proxies = proxy)
    
- web客户端验证
    - 遇到web客户端验证，需要添加auth=(用户名，密码)
        auth=('name', '12346')
        rsp=requests.get('http://www.baidu.com', auth = auth)
        
# 7.5. cookie   
- requests可以自动处理cookie信息  

    - rsp = requests.get('http//:xxx')   
    - 如果对方服务器传送过来cookie信息，则可以通过反馈的cookie属性得到
    - 返回一个cookiejar的实例
        - cookiejar = rsp.cookies 
        - cookiejar的实例可以转成字典
        - cookiedict = requests.utils.dict_from_cookiejar(cookiejar)      
    
## 7.6. session
- 跟#4.中的服务器中的session不是一个东东
- 模拟一次会话，从客户端浏览器链接服务器开始，到客户端浏览器断开
- 上述过程中的信息保存在session中
    
    创建session对象，可以保持cookie值
    ss = requests.session()
    headers = {'User-Agent': 'xxxxxx'}
    data = {'name': 'xxxxx'}
    此时，由创建的session管理请求，负责发出请求
    ss.post('URL', data = data, headers = headers)
    rsp = ss.get('xxxxxx')
    
## 7.7. https请求验证ssl证书
- 参数verify负责表示是否需要验证ssl证书，默认是True
- 如果不需要验证ssl证书，则设置成False表示关闭
- 写法
        
        rsp = requests.get('https://www.12306.com', verify = False)
        
       
    
                  
                  
   
                  
    
    
    
    