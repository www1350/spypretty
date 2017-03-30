from lxml import etree
import requests
import os
class OneImgInfo(object):
    def __init__(self,name,tags,bannerPath,paths):
        self.name = name
        self.tags = tags
        self.bannerPath = bannerPath
        self.paths = paths





class PageInfo(object):
    def __init__(self,data):
        self.data = data
    def getPageMeta(self):
        content = self.data
        dom = etree.HTML(content)
        self.currentIndex = dom.xpath("//div[@class='NewPages']/ul/li[2]/a/text()")[0]
        self.nextUrl = dom.xpath("//div[@class='NewPages']/ul/li[last()-1]/a/@href")[0]
        imgs = []
        tags = []
        for eli in dom.xpath("//div[@class='TypeList']/ul/li"):
            name = eli.xpath("a/div/text()")[0]
            bannerPath = saveFile( eli.xpath("a/img/@src")[0] ,name ,"banner")
            realImgUrl = eli.xpath("a/@href")[0]
            paths = findAllImg(realImgUrl,name)

            for priTag in eli.xpath("//div[@class='TypePicTags']/a"):
                # print priTag.xpath("text()")[0]
                tags.append(priTag.xpath("text()")[0])
            oneimg = OneImgInfo(name,tags,bannerPath,paths)
            imgs.append(oneimg)
            # print eli.xpath("a/div/text()")[0]
            saveInfo(oneimg,name)
        self.imgs = imgs
def saveInfo(oneimg, name):
    path = name + "/info.txt"
    file = open(path, "w+")
    file.write("%s \n" % (oneimg.name.encode("utf8")))
    file.write("%s \n" % (oneimg.bannerPath.encode("utf8")))
    for tag in oneimg.tags:
        file.write("%s \n" % (tag.encode("utf8")))
    for path in oneimg.paths:
        file.write("%s \n" % (path.encode("utf8")))
    file.close()
def saveFile(url,name,picName):
    content = requests.get(url).content
    dir = "pic/"+name
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = dir+"/"+picName+".jpg"
    file = open(path, "wb")
    file.write(content)
    file.close()
    return path
def findAllImg(realImgUrl,name):
    paths = []
    while "#" != realImgUrl:
        dom = etree.HTML(requests.get(realImgUrl).content)
        realImgUrl = "http://www.umei.cc"+dom.xpath("//div[@class='NewPages']/ul/li[last()]/a/@href")[0]
        picAlt = dom.xpath("//div[@class='ImageBody']/p/img/@alt")[0]
        picSrc = dom.xpath("//div[@class='ImageBody']/p/img/@src")[0]
        paths.append(saveFile(picSrc,name,picAlt))
    return paths


