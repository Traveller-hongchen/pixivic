from urllib.parse import urlencode
import os
import re
import requests
import json


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
                url = re.findall("img-original/img(.+?)$",url)[0]
                url_rel = 'https://original.img.cheerfun.dev/img-original/img' + url
                urllist.append([url_rel,folder])
    return urllist

def download(urllists):
    header = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://pixivic.com/popSearch'
        }
    if urllists:
        for urllist in urllists:
            file_name = urllist[0].split('/')[-1]  # 提取文件名
            if urllist[1] != '0':
                isExists = os.path.exists('pic\\' + urllist[1])
                if not isExists:
                    os.makedirs('pic\\' + urllist[1])   #创建目录
                filename = r'pic\%s\%s' % (urllist[1], file_name)
            else:
                filename = r'pic\%s' % (file_name)
            url = urllist[0]
            print(url)
            pic = requests.get(url, headers=header)
            if pic.status_code == 200:
                with open(filename, 'wb') as fp:
                    print(filename + "正在下载")
                    fp.write(pic.content)
                    fp.close()
                print(filename + "下载完成")
key = ''
urllists = geturl(key,1)
isExist = os.path.exists('pic\\')
if not isExist:
    os.makedirs('pic\\')
download(urllists)
