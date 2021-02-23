import requests
from bs4 import BeautifulSoup
import random
from multiprocessing import Pool, cpu_count

##get proxy list from https://free-proxy-list.net/
def get_ip(url, ip=None, ua=None):
    res = requests.get(url, headers=ua, proxies=ip).text
    soup = BeautifulSoup(res, 'lxml')
    my_ip = soup.find('table').find('tbody').find_all('tr')#.find('span').text
    with open('proxies.txt', 'a') as f:
        for i in my_ip:
            f.writelines(i.find_all('td')[:2][0].text + ':' + i.find_all('td')[:2][-1].text)
            f.writelines('\n')

##check is valid proxy from list
def main(ip):
    url = 'https://2ip.ru/'
    useragents = open('useragents.txt').read().split('\n')
    proxy = {
        'https': f'https://{ip}'
    }
    useragent = {
        'User-Agent': random.choice(useragents)
    }
    try:
        print(f'{get_ip(url, proxy, useragent)}')
    except Exception:
        print(f'ip is not availible')


if __name__ == "__main__":
     ip_list = open('proxies.txt').read().split('\n')[:-1]
     with Pool(cpu_count()) as process:
         process.map(main, ip_list)


#adsdqweqweew
