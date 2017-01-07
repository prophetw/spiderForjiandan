#coding:UTF-8
from bs4 import BeautifulSoup
import requests as rs
import re
import os

# args
imagebeginpage=2200
imageendpage=2300
votelimit = 300

def downloadImg(url,dirName,prefixName,extraName,description):
    # Todo how to write description to a image file
    # should add this info the original link 'http://jandan.net/ooxx/page-2307#comment-3362040' to the image description
    # 暂时的方案是 把链接存到文件名 这样就可以通过文件名 来找到网页的图片了
    # 例如 http://jandan.net/ooxx/page-2307#comment-3362040
    # 存成 ooxx/page-2307#comment-3362040.jpg
    r = rs.get(url)
    if os.path.exists(dirName)==False:
        os.makedirs(dirName)
    with open(dirName+'/'+prefixName+'.'+extraName, "w") as code:
        code.write(r.content)
def getPreNameFrom(url):
    arr = url.split('/')
    name = arr[len(arr)-1]
    return name
def getDirFrom(url):
    arr = url.split('/')
    dirName = arr[len(arr)-2]
    return dirName
def getFileExt(url):
    arr = url.split('.')
    extraName = arr[len(arr)-1]
    return extraName
def rename(id,vote):
    return id+'-vote-'+vote

def getImg(requestUrl):
    theHtml = rs.get(requestUrl).text
    # BeautifulSoup to get the page html
    soup = BeautifulSoup(theHtml, 'lxml')
    soup.prettify()
    theCommentList = soup.find('ol', class_='commentlist')
    allLiTag = theCommentList.find_all('li')
    for li in allLiTag:
        if li.get('id')=='adsense':
            continue
        vote = li.find('div', class_='vote').find_all('span')[1].string
        vote = int(vote)
        if vote>votelimit:
            try:
                id = li.get('id')
                # print(id)
                originalLink = li.find('span', class_='righttext').find('a').get('href')
                dirName = getDirFrom(originalLink)
                name = getPreNameFrom(originalLink)
                imageUrl = li.find('a', class_='view_img_link').get('href')
                vote = li.find('div', class_='vote').find_all('span')[1].string
                prefixName= rename(name,vote)
                extraName = getFileExt(imageUrl)
                downloadImg('http:'+imageUrl,dirName,prefixName,extraName,originalLink)
                print(vote)
            except:
                continue
        else:
            continue

while(imagebeginpage<imageendpage):
    beginPage = str(imagebeginpage)
    print(imagebeginpage)
    # 妹纸
    # 'http://jandan.net/ooxx/page-' + beginPage + '#comments'
    # 无聊
    # 'http://jandan.net/pic/page-' + beginPage + '#comments'
    requestUrl = 'http://jandan.net/ooxx/page-' + beginPage + '#comments'
    getImg(requestUrl)
    imagebeginpage +=1

