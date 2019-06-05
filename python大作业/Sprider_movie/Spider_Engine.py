# encoding=utf-8
# by:KuroNeko
import threading
import urllib.request

import datetime
import pymysql
import json

import time
from lxml import etree

lock = threading.Lock()  # 数据库的锁，只允许同时有一个线程操作数据库
lock_num = threading.Lock()  # 全局变量,爬取电影的计数锁
NUM = 0


# 爬虫客户端爬取模块
class Spider(object):
    # 编辑头。使其不会被网站拦截
    def __init__(self):
        self.send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Referer': 'https://movie.douban.com/explore'
        }
        self.hotMovieUrl_list = []
        self.movieDetailInfo_list = []
        global lock
        global lock_num

    # 爬取热门电影列表(参数：电影种类，排序方式，页数)【第一层】
    def getHotMovieUrlList(self, movie_type, movie_sort, pageNum):
        if int(pageNum) > 0:  # 当页数大于0时才能爬取
            for i in range(int(pageNum)):
                print(i)  # 输出页数
                start = i * 20
                url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + movie_type + '&sort=' + movie_sort + '&page_limit=20&page_start=' + str(
                    start)
                print(url)
                # 使用Request类构建一个完整的请求 增加headers信息
                req = urllib.request.Request(url, headers=self.send_headers)
                # 打开url获得响应
                resp = urllib.request.urlopen(req)
                # 接受响应信息
                json_data = resp.read().decode('utf-8')
                # 将json数据转换成字典
                json_obj = json.loads(
                    json_data)  # 转换为字典后，是以列表的方式返回，且这个列表中就一个字典元素：subjects，该字典对应一个列表，这个列表对应一个字典，表示该电影所有信息
                for key, value in json_obj.items():
                    # print(value)
                    for item in value:
                        # print(item)#具体电影信息，包括电影名和详细信息的URL地址
                        hotMovie_dict = {}
                        hotMovie_dict['url'] = item['url']
                        self.hotMovieUrl_list.append(hotMovie_dict)
        else:  # 页数小于等于0直接返回
            return False
        # 返回id+name的list表
        return self.hotMovieUrl_list

    # 爬取热门电影详细信息【第二层】
    def getMovieDetailInfo(self, movie_url, page_info):
        movieDetailInfo_dict = {}  # 存储电影详细信息的字典
        resp = urllib.request.urlopen(movie_url)
        html_data = resp.read().decode('utf-8')
        # 构建xpath
        html = etree.HTML(html_data)
        # movie_year = soup.find('span', class_='year').text.strip('(').strip(')')
        movie_year = html.xpath('//*[@id="content"]/h1/span[2]/text()')[0].strip('(').strip(')')  # 年份
        #  print(movie_year)
        movieDetailInfo_dict['movie_year'] = movie_year
        # movie_name = soup.find('i',class_='').text.split('的')[0]
        if (page_info[5]):
            movie_name = html.xpath('//*[@id="content"]/h1/span[1]/text()')[0].split(' ')[0]  # 电影名
            #  print(movie_name)
            movieDetailInfo_dict['movie_name'] = movie_name
        else:
            movieDetailInfo_dict['movie_name'] = ""
        # movie_director
        if (page_info[6]):
            movie_director_list = html.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')  # 导演
            director = ""
            for directors in movie_director_list:
                director += str(directors) + "/"

            movie_director = director.strip('/')
            #   print(movie_director)
            movieDetailInfo_dict['movie_director'] = movie_director
        else:
            movieDetailInfo_dict['movie_director'] = ""
        movie_writer_list = html.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')  # 编剧
        writer = ""
        for writers in movie_writer_list:
            writer += str(writers) + "/"

        movie_writer = writer.strip('/')
        # print(movie_writer)
        movieDetailInfo_dict['movie_writer'] = movie_writer
        # movie_actor = //*[@id="info"]/span[3]/span[2]
        if (page_info[7]):
            movie_actor_list = html.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')  # 演员
            actor = ""
            for actors in movie_actor_list:
                actor += str(actors) + "/"

            movie_actor = actor.strip('/')
            #  print(movie_actor)
            movieDetailInfo_dict['movie_actor'] = movie_actor
        else:
            movieDetailInfo_dict['movie_actor'] = ""
        # movie_type = //*[@id="info"]/span[5]
        movie_type_list = html.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')  # 类型
        type = ""
        for types in movie_type_list:
            type += str(types) + "/"

        movie_type = type.strip('/')
        #  print(movie_type)
        movieDetailInfo_dict['movie_type'] = movie_type
        # movie_country = //*[@id="info"]/span[7] //*[@id="info"]/span[8]
        movieDetailInfo_dict['movie_anotherName'] = ""  # 别名
        movieDetailInfo_dict['movie_language'] = ""  # 语言
        movieDetailInfo_dict['movie_country'] = ""  # 国家/地区
        movie_attrs = html.xpath('//*[@id="info"]/span[@class="pl"]')
        for attr in movie_attrs:
            # print(attr.text)
            if attr.text == '制片国家/地区:' and page_info[8]:
                movie_country = attr.tail.strip()
                #   print(movie_country)
                movieDetailInfo_dict['movie_country'] = movie_country
            if attr.text == '语言:':
                movie_language = attr.tail.strip()
                #  print(movie_language)
                movieDetailInfo_dict['movie_language'] = movie_language
            if attr.text == '又名:':
                movie_anotherName = attr.tail.strip()
                #  print(movie_anotherName)
                movieDetailInfo_dict['movie_anotherName'] = movie_anotherName

        # movie_date = //*[@id="info"]/span[10]
        try:
            movie_date = html.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[0]
            # print(movie_date)
            movieDetailInfo_dict['movie_date'] = movie_date  # 上映日期
        except:
            movieDetailInfo_dict['movie_date'] = "无上映日期"
        try:
            # movie_time = v:runtime
            movie_time = html.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
            # print(movie_time)
        except:
            movie_time = "无片长信息"
        movieDetailInfo_dict['movie_time'] = movie_time  # 片长
        # movie_IMDB = //*[@id="info"]/a
        movieDetailInfo_dict['movie_IMDB'] = ""
        movie_IMDB = html.xpath('//*[@id="info"]/a[@rel="nofollow" and @target="_blank"]/text()')
        if len(movie_IMDB) != 0:
            # print(movie_IMDB)
            movieDetailInfo_dict['movie_IMDB'] = movie_IMDB[0]  # IMDB链接
        # movie_grade =
        movie_grade = html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        # print(movie_grade)
        movieDetailInfo_dict['movie_grade'] = movie_grade  # 评分
        # movie_commentsNum = //*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span
        movie_commentsNum = html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
        # print(movie_commentsNum)
        movieDetailInfo_dict['movie_commentsNum'] = movie_commentsNum  # 评价人数
        # movie_pageUrl = movie_url
        movie_pageUrl = movie_url
        # print(movie_pageUrl)
        movieDetailInfo_dict['movie_pageUrl'] = movie_pageUrl  # 电影详情页面URL地址

        if (page_info[9]):
            movieDetailInfo_dict['movie_comment'] = self.get_comments(movie_url + 'comments?status=F')  # 短评
        else:
            movieDetailInfo_dict['movie_comment'] = ""
        # print(movieDetailInfo_dict['movie_comment'])

        if (page_info[10]):
            movieDetailInfo_dict['movie_discussion'] = self.get_discussion(movie_url + 'discussion/')  # 论坛
        else:
            movieDetailInfo_dict['movie_discussion'] = ""
        # print(movieDetailInfo_dict['movie_discussion'])

        movieDetailInfo_dict['actor_url'] = html.xpath('//*[@id="info"]/span[3]/span[2]/a/@href')
        # print(movieDetailInfo_dict['actor_url'])
        movieDetailInfo_dict['actor_message'] = []
        for it in movieDetailInfo_dict['actor_url']:
            if page_info[4]: time.sleep(3)
            actor_info = {}
            actor_info['name'] = ""
            actor_info['sex'] = ""
            actor_info['star'] = ""
            actor_info['birthday'] = ""
            actor_info['place'] = ""
            actor_info['job'] = ""
            actor_info['message'] = ""
            resp2 = urllib.request.urlopen('https://movie.douban.com/' + it)
            html_data2 = resp2.read().decode('utf-8')
            html2 = etree.HTML(html_data2)
            try:
                actor_info['name'] = html2.xpath('//*[@id="content"]/h1/text()')[0]  # 姓名
                actor_info['sex'] = html2.xpath('//*[@id="headline"]/div[2]/ul/li[1]/text()')[1].strip('\n').strip(':').strip()  # 性别
                actor_info['star'] = html2.xpath('//*[@id="headline"]/div[2]/ul/li[2]/text()')[1].strip('\n').strip(':').strip()  # 星座
                actor_info['birthday'] = html2.xpath('//*[@id="headline"]/div[2]/ul/li[3]/text()')[1].strip('\n').strip(':').strip()  # 生日
                actor_info['place'] = html2.xpath('//*[@id="headline"]/div[2]/ul/li[4]/text()')[1].strip('\n').strip(':').strip()  # 出生地
                actor_info['job'] = html2.xpath('//*[@id="headline"]/div[2]/ul/li[5]/text()')[1].strip('\n').strip(':').strip()  # 职业
                try:actor_info['message'] = html2.xpath('//*[@id="intro"]/div[2]/span[2]/text()')[0].replace('\u3000',''), replace('\n', '').strip()  # 简介
                except:actor_info['message'] = html2.xpath('//*[@id="intro"]/div[2]/text()')[0].replace('\u3000','').replace('\n','').strip()
            except:
                print('https://movie.douban.com/' + it, '无该演员信息')
            if actor_info:
                movieDetailInfo_dict['actor_message'].append(actor_info)
            else:
                pass
            if page_info[4] == 0: break
        print(movieDetailInfo_dict['actor_message'])

        return movieDetailInfo_dict
        # 爬取结果是字典，表示单部电影的所有详细信息

    def get_comments(self, comments_url):  # 第一条短评【P为看过，F为想看】
        resp = urllib.request.urlopen(comments_url)
        html_data = resp.read().decode('utf-8')
        # 构建xpath
        html = etree.HTML(html_data)
        return html.xpath('//*[@id="comments"]/div[1]/div[2]/p/span/text()')[0]

    def get_discussion(self, discussion_url):  # 论坛第一条题目
        resp = urllib.request.urlopen(discussion_url)
        html_data = resp.read().decode('utf-8')
        # 构建xpath
        html = etree.HTML(html_data)
        try:
            return html.xpath('//*[@id="posts-table"]//tr[2]/td[1]/a/text()')[0].strip('\n').strip()
        except:
            return "论坛内容为空"

    # 插入数据库
    def saveDatabase(self, movie_info, conn):
        lock.acquire()
        cur = conn.cursor()
        # print(movie_info['movie_anotherName'],'='*20)
        actor_info = movie_info['actor_message']
        for it in actor_info:
            sql_select = 'select name from actors where name="%s"' % (it['name'])
            cur.execute(sql_select)
            conn.commit()
            check_name = cur.fetchone()
            if check_name == None:
                sql_actor = 'insert into actors values(null,"%s","%s","%s","%s","%s","%s","%s")' % (
                    it['name'], it['sex'], it['star'], it['birthday'], it['place'], it['job'], it['message'])
                try:
                    cur.execute(sql_actor)
                    conn.commit()
                    print(it['name'], '保存成功呢')
                except:
                    print('演员信息不完整')
        try:
            sql_judge = 'select movie_name from movies where movie_name="%s"' % (movie_info['movie_name'])
            cur.execute(sql_judge)
            conn.commit()
            judge_name = cur.fetchone()
            if judge_name == None:
                sql = 'insert into movies values(null ,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    movie_info['movie_year'], movie_info['movie_name'], movie_info['movie_director'],
                    movie_info['movie_writer'], movie_info['movie_actor'], movie_info['movie_type'],
                    movie_info['movie_country'], movie_info['movie_language'], movie_info['movie_anotherName'],
                    movie_info['movie_date'], movie_info['movie_time'], movie_info['movie_IMDB'],
                    movie_info['movie_grade'],
                    movie_info['movie_commentsNum'], movie_info['movie_pageUrl'], movie_info['movie_comment'],
                    movie_info['movie_discussion'])
                cur.execute(sql)
                conn.commit()
                print("保存成功！！！")
        except:
            try:
                sql_judge = 'select movie_name from movies where movie_name="%s"' % (movie_info['movie_name'])
                cur.execute(sql_judge)
                conn.commit()
                judge_name = cur.fetchone()
                if judge_name == None:
                    sql = 'insert into movies values(null ,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        movie_info['movie_year'], movie_info['movie_name'], movie_info['movie_director'],
                        movie_info['movie_writer'], movie_info['movie_actor'], movie_info['movie_type'],
                        movie_info['movie_country'], movie_info['movie_language'], movie_info['movie_anotherName'],
                        movie_info['movie_date'], movie_info['movie_time'], movie_info['movie_IMDB'],
                        movie_info['movie_grade'],
                        movie_info['movie_commentsNum'], movie_info['movie_pageUrl'], "评论存在emoji或未知编码字符",
                        movie_info['movie_discussion'])
                    cur.execute(sql)
                    conn.commit()
                    print("保存成功！！！")
            except:
                print("保存失败！！！")
        lock.release()
        cur.close()
        return movie_info

    def getMovieDetailInfo_list(self, movie_urls, connClient, page_info):
        conn = pymysql.connect(host='localhost', user='root', password='970922', db='mytest', port=3306, charset='utf8')
        for url in movie_urls:
            time.sleep(1)
            movieDetailInfo = self.getMovieDetailInfo(url['url'], page_info)  # 【第二层】爬取详细信息
            movie_info = self.saveDatabase(movieDetailInfo, conn)  # 存储到数据库中
            # movie_info['movie_year'] ,movie_info['movie_name'] ,movie_info['movie_director'] ,movie_info['movie_writer'] ,movie_info['movie_actor']  ,movie_info['movie_type'] ,movie_info['movie_country'] ,	movie_info['movie_language'] ,movie_info['movie_anotherName'] ,	movie_info['movie_date'] ,movie_info['movie_time'] ,movie_info['movie_IMDB'] ,movie_info['movie_grade'] ,movie_info['movie_commentsNum'] ,movie_info['movie_pageUrl']
            lock_num.acquire()
            global NUM
            NUM = NUM + 1
            num = NUM  # 从这里开始构建返回到客户端的信息
            movie_msg = '爬取的第' + str(num) + '条电影信息\n'
            movie_msg += '|' + '>' * 60 + '|\n'
            movie_msg += '【上映年份】' + movie_info['movie_year'] + '\n【片名】' + movie_info['movie_name'] + '\n【导演】' + \
                         movie_info['movie_director'] + '\n【编剧】' + movie_info['movie_writer'] + '\n【主演】' + movie_info[
                             'movie_actor'] + '\n【类型】' + movie_info['movie_type'] + '\n【制片国家地区】' + movie_info[
                             'movie_country'] + '\n【语言】' + movie_info['movie_language'] + '\n【上映日期】' + movie_info[
                             'movie_date'] + '\n【片长】' + movie_info['movie_time'] + '\n【又名】' + movie_info[
                             'movie_anotherName'] + '\n【IMDB链接】' + movie_info['movie_IMDB'] + '\n【评分】' + movie_info[
                             'movie_grade'] + '\n【评价人数】' + movie_info['movie_commentsNum'] + '\n【页面网址】' + movie_info[
                             'movie_pageUrl'] + '\n【短评】' + movie_info['movie_comment'] + '\n【论坛讨论】' + movie_info[
                             'movie_discussion'] + '\n'
            movie_msg += '|' + '<' * 60 + '|\n'
            print(movie_msg)
            lock_num.release()
            threading.Thread(target=connClient.sendall, args=(movie_msg.encode(),)).start()  # 启动线程发送回客户端显示
            print(movie_urls.index(url))
        print('结束')
        connClient.sendall("end".encode())  # 一个线程的结束
        conn.close()

    # page_info[movie_type,movie_sort,threadNum,pageNum,query_type]
    def startSpiderInfo(self, page_info, connClient):  # 此处是被服务器端启动的爬虫线程
        # print(page_info)
        global NUM
        NUM=0
        urls = self.getHotMovieUrlList(page_info[0], page_info[1], page_info[3])  # 首先爬取电影列表【第一层】
        print(urls)  # 返回要爬取详细信息的电影URL列表，是以字典形式存储
        for i in range(int(page_info[2])):  # page_info[2]就是线程数
            time.sleep(1)
            leng = len(urls)
            movie_urls = urls[i * leng // int(page_info[2]):(i + 1) * leng // int(page_info[2])]  # 切片操作，为每个线程平均分配要爬的电影url
            threading.Thread(target=self.getMovieDetailInfo_list, args=(movie_urls, connClient, page_info,)).start()
            # 创建并启动线程，调用获取电影详细信息【第二层】
