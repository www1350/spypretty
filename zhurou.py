# -*- coding:UTF-8 -*-
import time
from lxml import etree

import requests


def spyPig(url, fileName,pageNo):
    url = url +"&page="+str(pageNo)
    file = open(fileName, "a")
    encode = requests.get(url).encoding
    content  = requests.get(url).content
    dom = etree.HTML(content)
    list = dom.xpath("//div[@class='mess brtb']/div[@class='cpu-feeds-block']/following-sibling::*/following-sibling::*/p")
    for p in list:
        text = p.xpath("text()")[0].encode("utf8")
        if "元/公斤" in text:
            print text
            file.write("%s \n" % (text))
    file.close()

def is_dig(n):
    return n.isdigit()

def spyPage(url):
    content = requests.get(url).content
    dom = etree.HTML(content)
    nextPageList = dom.xpath("//div[@class='mess brtb']/center")[0].xpath('string(.)').replace('\n','').replace(' ','').replace('[',' ').replace(']',' ')
    nextPageSp =  nextPageList.split(' ')
    nextPage = filter(is_dig, nextPageSp)
    print nextPage[-1]
    return int(nextPage[-1])



def main():
    url = "http://m.zhujiage.com.cn"
    content = requests.get(url).content
    dom = etree.HTML(content)
    url =  "http://m.zhujiage.com.cn/index.php?action=article&id=" + dom.xpath("//ul[@class='p_newslist']/li/a/@href")[0].replace('/article/','').replace('.html','')
    print url
    # url = "http://m.zhujiage.com.cn/index.php?action=article&id=734860"
    timeName = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    fileName = "pig"+timeName+".txt"
    file = open(fileName, "w")
    file.write(timeName+"猪肉价格")
    file.close()
    print timeName
    lastPage = spyPage(url)
    for page in range(1,lastPage+1):
        print page
        spyPig(url,fileName,page)


if __name__ == '__main__':
    main()