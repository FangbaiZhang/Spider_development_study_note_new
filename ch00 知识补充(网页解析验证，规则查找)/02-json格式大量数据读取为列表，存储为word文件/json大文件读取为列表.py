import json
import docx

# 将json文件读取出来，然后提取部分内容，最后写入到word文件中
# 将json文件复制到改代码文件目录下

# 由于文件中有多行，直接读取会出现错误，因此一行一行读取
def read_json():
    # 读取json文件，加入到列表中,注意文件名称前面加一个r,去掉\作为转义符的含义，有时候需要路径打开要使用\
    # papers.json来自ch12爬取后存储的结果，复制到该目录下即可
    file = open(r'papers.json', 'r', encoding='utf-8')
    papers = []
    for line in file.readlines():
        dic = json.loads(line)
        papers.append(dic)
    print(len(papers))

    # 提取列表中的下载地址内容，写入到docx文件中
    file = docx.Document()
    for paper in papers:
        mag = str(paper['title']) + ":\n" + str(paper['content'])
        # 添加方式写入，自动换行
        file.add_paragraph(mag)
    file.save('国产原创.docx')

if __name__ == '__main__':
    read_json()



