import requests
import os
import json
from requests.exceptions import RequestException
from lxml import etree
from multiprocessing import Pool
from config import *

def get_page_index(url):
    headers = {
        # 'Cookie': 'uuid=1A6E888B4A4B29B16FBA1299108DBE9C8AABDEB9C9707986732AC54681EEBB13; _csrf=54de01012c7c2039b762731bc4f485f51c1376304b5610da867ed2bab5a30cf5; __mta=251378233.1510120992983.1510121649404.1510121659083.8; _lxsdk_s=e753196344bbd2420617863f3145%7C%7C19',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'maoyan.com',
        'Referer': 'http://maoyan.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None


def get_movies_info(text):
    info = []

    # 将传入的文本转成 xpath 对象
    html = etree.HTML(text)

    # 所有页面中的电影内容部分
    movies = html.xpath('//dl/dd')

    # 遍历每一部电影并拿到想要的星星
    for movie in movies:
        # 用来存储一部电影的信息
        msg = dict()

        # 电影详细页面 url
        url = 'http://maoyan.com' + movie.xpath('./a[1]/@href')[0]
        # 电影排名
        index = movie.xpath('./i/text()')[0]
        # 电影名
        title = movie.xpath('./a[1]/@title')[0]
        # 演员明星
        star = movie.xpath('.//p[@class="star"]/text()')[0]
        # 上映时间
        releasetime = movie.xpath('.//p[@class="releasetime"]/text()')[0]
        # 评分
        score = movie.xpath('.//p[@class="score"]/i/text()')[0] + movie.xpath('.//p[@class="score"]/i/text()')[1]

        msg['index'] = index
        msg['title'] = title.strip()
        msg['url'] = url.strip()
        msg['star'] = star.strip()
        msg['time'] = releasetime.strip()
        msg['score'] = score.strip()

        info.append(msg)

    return info


def save_movie_info(path, info):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileNotFoundError:
            print('无法创建该路径')

    # 以 utf-8 打开文件，并在 json.dumps 方法中传入 ensure_ascii=False 参数可以把汉字以 utf-8 编码写入文件中
    with open(path+'/movies.txt', 'a', encoding='utf-8') as f:   # 
        for i in info:
            t = json.dumps(i, ensure_ascii=False)
            f.write(t+'\n')
    print('写入成功')


def main(offset):
    base_url = 'http://maoyan.com/board/4?offset='
    url = base_url + str(offset)
    text = get_page_index(url)
    info = get_movies_info(text)
    save_movie_info(PATH, info)


if __name__ == '__main__':
    # main()
    pool = Pool()
    pool.map(main, [num*10 for num in range(10)])