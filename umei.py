import requests
import pageinfo
def spider(start_url):
    response = requests.get(start_url)
    content  = requests.get(start_url).content
    # print "response headers:", response.headers
    # print "content:", content
    pinfo = pageinfo.PageInfo(content)
    pinfo.getPageMeta()
    print pinfo.currentIndex
    print pinfo.nextUrl
    if "" == pinfo.nextUrl:
        return
    spider("http://www.umei.cc"+pinfo.nextUrl)


if __name__ == '__main__':
    print "begin>>>"
    start_url = "http://www.umei.cc/tags/juru.htm"
    spider(start_url)
    print ">>>>end"