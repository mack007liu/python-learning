import argparse
import re
from multiprocessing import Pool
import requests
import bs4
import time
import json
import urllib2

root_url = 'http://wufazhuce.com'


def get_url(num):
    return root_url + '/one/' + str(num)


def get_urls(num):
    urls = map(get_url, range(100, 100 + num))
    return urls


def get_data(url):
    dataList = {}
    response = requests.get(url)
    if response.status_code != 200:
        return {'noValue': 'noValue'}
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup.title
    dataList["index"] = soup.title.string[4:7]
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = meta.get('content')
    dataList["imgUrl"] = soup.find_all('img')[1]['src']
    return dataList

def download():
    print "downloading with urllib2"
    url = 'http://www.spfctw.org/mp3/sundayschool/100531_biblecounselling7.mp3'
    #http://www.spfctw.org/mp3/sundayschool/100503_biblecounselling3.mp3
    start = time.time()
    f = urllib2.urlopen(url)
    data = f.read()
    with open("7.mp3", "wb") as code:
        code.write(data)
    end = time.time()
    print 'use: %.2f s' % (end - start)
    print "dowloaded success!"

if __name__ == '__main__':
    pool = Pool(4)
    dataList = []
    urls = get_urls(10)
    start = time.time()
    dataList = pool.map(get_data, urls)
    end = time.time()
    print 'use: %.2f s' % (end - start)
    jsonData = json.dumps({'data': dataList}).decode('unicode-escape')
    with open('data.txt', 'w') as outfile:
        json.dump(jsonData, outfile)
        print jsonData
    #download()