from proxy.generate_proxies import gen_proxies
import requests
from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Pool
import feedparser
import json
import random

# populate proxies
#proxies = gen_proxies()

# Get the latest feed post ID
def get_latest_from_feed():
    url = 'http://feeds.feedburner.com/ufostalker'
    d = feedparser.parse(url)
    latest_link = d['entries'][0]['link'].split('/')
    latest_id = latest_link[-1]
    return int(latest_id)

# Get a proxy value from the generated list
def get_proxy(protocol):
    http = []
    https = []
    lines = open('proxy/proxies.txt').readlines()
    for line in lines:
        if 'https' not in line:
            http.append(line)
        else:
            https.append(line)
    if protocol == 'http':
        ip = str(random.choice(http))
    if protocol == 'https':
        ip = str(random.choice(https))
    return ip



def get_listing():
    links = []
    for i in range(get_latest_from_feed() - 100, get_latest_from_feed()):
        links.append('http://ufostalker.com:8080/event?id={}'.format(i))
    print(links)
    return links


# parse a single item to get information
def parse(url):
    print('running')
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    info = []
    title_text = '-'
    while True:
        try:
            http_proxy  = get_proxy('http')
            https_proxy = get_proxy('https')

            proxyDict = {
                        "http"  : "{}".format(http_proxy.rstrip()),
                        # "https" : "{}".format(https_proxy.rstrip())
                        }
            print(proxyDict)

            r = requests.get(url, headers=headers, timeout=20, proxies=proxyDict)
            sleep(15)

            if r.status_code == 200:
                print('Processing..' + url)
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
                title = soup.find('summary')
                if title is not None:
                    title_text = title.text.strip()
                else:
                    title_text = 'no title'

                info.append(url)
                info.append(title_text)
            else:
                info.append(url)
                info.append('failed')
        except Exception as ex:
            print(str(ex))
            print('ERRRRROOOOOOOR')
            continue
        finally:
            if len(info) > 0:
                return ','.join(info)
            else:
                return None
        break

car_links = None
cars_info = []
cars_links = get_listing()


with Pool(10) as p:
    sleep(5)
    records = p.map(parse, cars_links)
    p.terminate()
    p.join()


with open('data.json', 'w') as outfile:
    json.dump(records, outfile)

# with open('proxy/proxies.txt','r') as reader :
#     for line in reader :
#         proxy = line.split('\n', 1)[0]
#         http_proxy =  'http://'+proxy
#         https_proxy = 'https://'+proxy

#         proxies = {
#             'http': http_proxy,
#             'https': https_proxy,
#         }

#         print(proxies)