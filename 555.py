from gevent import monkey
monkey.patch_all
import gevent,time,requests,csv
from gevent.queue import Queue
from bs4 import BeautifulSoup

url_list = []
url_1 = 'http://www.mtime.com/top/tv/top100/'
url_list.append(url_1)
for page in range(2,11):
        url_0 = 'http://www.mtime.com/top/tv/top100/index-{}.html'.format(page)
        url_list.append(url_0)
work = Queue()
for url in url_list:
        work.put_nowait(url)

csv_file = open('1111111.csv','w',newline = '',encoding = 'utf-8')
writer = csv.writer(csv_file)

def crawler():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        while not work.empty():
                url = work.get_nowait()
                r = requests.get(url,headers = headers)
                soup = BeautifulSoup(r.text,'html.parser')
                url_list1 = soup.find_all('div',class_="mov_con")
                for Tag in url_list1 :
                        n = Tag.find('a')
                        a = n.text
                        lists = Tag.find_all('p')
                        try:
                                a_3 = (Tag.find('p',class_="mt3")).text
                        except:
                                a_3 = ''
                        for i in lists[0:1]:
                                a_1 = i.text
                        for r in lists[1:2]:
                                a_2 = r.text
                        writer.writerow([a,a_1,a_2,a_3])

tasks_list = []
for x in range(3):
        task = gevent.spawn(crawler)
        tasks_list.append(task)
gevent.joinall(tasks_list)