from gevent import monkey
monkey.patch_all()
import gevent,time,requests,csv
from gevent.queue import Queue
from bs4 import BeautifulSoup

csv_file = open ('3.8.csv','w',newline = '',encoding = 'utf-8')
writer = csv.writer(csv_file)
writer.writerow(['名称','热量','详情'])
url_list = []
for page in range(1,4):
    for page_2 in range (1,4):
        url = 'http://www.boohee.com/food/group/{}?page={}'.format(page,page_2)
        url_list.append(url)
    url_menu = 'http://www.boohee.com/food/view_menu?page={}'.format(page)
    url_list.append(url_menu)
work = Queue()
for url in url_list:
    work.put_nowait(url)
def crawler():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    while not work.empty():
        url = work.get_nowait()
        r = requests.get(url,headers = headers)
        soup = BeautifulSoup(r.text,'html.parser')
        list_a = soup.find_all('li',class_="item clearfix")
        for Tag in list_a :
            a = Tag.find('h4')
            a_1 = a.text[1:-1]
            c = a.find('a')
            c_1 = c['href']
            c_2 = 'http://www.boohee.com'+c_1
            b = Tag.find('p')
            b_1 = b.text[3:]
            writer.writerow([a_1,b_1,c_2])
tasks_list = []
for x in range (2):
    task = gevent.spawn(crawler)
    tasks_list.append(task)
gevent.joinall(tasks_list)
csv_file.close()