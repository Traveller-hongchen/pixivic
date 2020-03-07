from urllib.parse import urlencode
import os
import re
import requests
import json
import threading


class MyThread(threading.Thread):
    def __init__(self, namepians, urlpians,id):
        """
        :param thread_id:
        :param name:
        :param counter:
        """
        threading.Thread.__init__(self)
        self.namepians = namepians
        self.urlpians = urlpians
        self.id = str(id+1)

    def run(self):
        """
        :return:
        """
        print("开始线程：{}".format(self.id))
        download(self.urlpians,self.namepians)
        print("退出线程：{}".format(self.id))
#获取图片链接
def geturl(keyword,pages):
    pages = int(pages)+1
    for page in range(1,pages):
        urlend = {'keyword': keyword, 'page': page}
        urlst = 'https://api.pixivic.com/illustrations?'
        url = urlst + urlencode(urlend)
        txt = requests.get(url).text
        result = json.loads(txt)
        urllist = []
        for image in result.get('data'):
            for i in range(len(image.get('imageUrls'))):
                folder = "0"
                url = str(image.get('imageUrls')[i].get('original'))
                if len(image.get('imageUrls')) > 1:
                    folder = re.findall("(\d+?)_p",url)[0]
                try:
                    url = re.findall("img-original/img(.+?)$",url)[0]
                except IndexError:
                    print(url)
                url_rel = 'https://original.img.cheerfun.dev/img-original/img' + url
                urllist.append([url_rel,folder])
    return urllist

def getname(urllists,mulu):
    filenames = []
    if urllists:
        for urllist in urllists:
            file_name = urllist[0].split('/')[-1]  # 提取文件名
            if urllist[1] != '0':
                isExists = os.path.exists(mulu + urllist[1])
                if not isExists:
                    os.makedirs(mulu + urllist[1])   #创建目录
                filename = mulu + r'%s\%s' % (urllist[1], file_name)
            else:
                filename = mulu + r'%s' % (file_name)
            filenames.append(filename)
    return filenames

def download(picurl,name):
    header = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://pixivic.com/popSearch',
        'host' : 'original.img.cheerfun.dev'
    }
    #print(len(picurl))
    for i in range(0,len(picurl)):
        if not os.path.isfile(name[i]):
            pic = requests.get(picurl[i], headers=header)
            if pic.status_code == 200:
                print(name[i] + "开始下载")
                with open(name[i], 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
                print(name[i] + "下载完成")
    print("该线程下载完成")


def getpicurl(urllists):
    urls = []
    for urllist in urllists:
        urls.append(urllist[0])
    return urls


def qiepain(names,picurls,road):
    lenurls = len(picurls)
    if lenurls == len(names):
        len1 = lenurls // road
        apd = lenurls % road
        namepians = []
        urlpians = []
        start1 = 0
        for i in range(0,road):
            if apd > 0:

                namepians.append(names[start1 : start1 + len1 + 1])
                urlpians.append(picurls[start1 : start1 + len1 + 1])
                apd = apd - 1
                start1 = start1 + len1 + 1
            else:
                namepians.append(names[start1 : start1 + len1])
                urlpians.append(picurls[start1 : start1 + len1])
                start1 = start1 + len1
        return namepians,urlpians
    else:
        print("发生了某些不知名的错误导致文件链接和文件名数目不匹配")

def getThread(namepians,urlpians,road):
    for i in range(0,road):
         yield MyThread(namepians[i],urlpians[i],i)
if __name__ == '__main__':
    key = '东方'
    road = int('8')
    urllists = geturl(key,1)
    mulu = 'pic\\{}\\'.format(key)
    isExist = os.path.exists(mulu)
    if not isExist:
        os.makedirs(mulu)
    names = getname(urllists,mulu)
    picurls = getpicurl(urllists)
    #download(picurls,names)
    namepians,urlpians  = qiepain(names,picurls,road)
    threads = getThread(namepians,urlpians,road)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('主线程结束')
