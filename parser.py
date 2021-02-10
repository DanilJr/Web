import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import json
import sqlite3
from dishes import Dish
import csv
import random
from random import uniform


URL='https://www.russianfood.com/recipes/bytype/?fid=927#rcp_list'
HEADERS={
    #'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'accept': '*/*'
    }


def get_content():
    
    for i in range(2, 15):
        response = requests.get(f'https://www.russianfood.com/recipes/bytype/?fid=928&page={i}#rcp_list', headers=HEADERS)
        src = response.text
        time.sleep(10)
        with open(f'dates/{i}st.html', 'w') as f:
            f.write(src)
 
#get_content()


def get_info():
    dishes = {}
    for i in range(1, 15):

        with open(f'dates/dinners/{i}st.html') as f:
            src = f.read()
        soup = BeautifulSoup(src, 'html.parser')

        lanches = soup.find_all(class_="title")
        print(len(lanches))
        for _ in lanches:
            links = str(_.find('a')).split('"')
            names = _.text
            name = names.strip().split('\xa0НОВЫЙ')
            try:
                dishes[name[0]] = links[1]
                print(f'{name[0]}{links[1]}')
            except IndexError:
                print(f'{name[0]}{None}')
    return dishes        
            

class Parser:
    
    #def __init__(self, url=None):
    #     time.sleep(random.randrange(3,5)
    #     #if url is not None:
    #     self.html = requests.get(url, headers=HEADERS).text
    #     self.soup = BeautifulSoup(self.html, 'html.parser')
    #     #else:
    #         print('url is None')

   #proxies={'https':f'84.247.51.123:3128'}


    def __init__(self, url=None, proxy=None):
        time.sleep(random.uniform(3, 6))
        self.html = requests.get(url, headers=HEADERS, proxies={'https':proxy}).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
    

    def get_soup(self, html):
        with open(html) as file:
            return file.read()


    def get_name(self):
        try:
            name = self.soup.find('h1', class_='title')
            name = name.text
            return name
        except AttributeError:
            return 'Name is lost'

    def get_discription(self):
        discription = self.soup.find('td', class_='padding_r').find('p')
        discription = discription.text
        return discription


    def get_ingridients(self):
        ing = []
        ingridients = self.soup.find('table', class_='ingr').find_all('span')
        for i in ingridients:
            ing += [i.text]
        return ing


    def get_steps(self):
        st = []
        steps = self.soup.find('div', class_='step_images_n')

        try:
            for el in steps.find_all('p'):
                st += [el.text]
        except AttributeError:
            st += [None]
        return st


    def get_img(self):
        link = str(self.soup.find(class_='main_image')).split('//')
        link_img = link[1].split('"')[0]
        return link_img


    def get_all(self):
        return self.get_name(), self.get_discription(), self.get_ingridients(), self.get_steps(), self.get_img()


    def set_csv(self, name, discription, ing, steps, link):
        date = {
            'name':name,
            'discription':discription,
            'ingridients':ing,
            'steps':steps,
            'img_link':link
        }
        with open('DB/10.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                date['name'],
                date['discription'],
                date['ingridients'],
                date['steps'],
                date['img_link']
            ))
        return date

##url example 'https://www.russianfood.com'
def get_full_info(url):
    
    type_ = 'dinners'
    with open(f'dates/{type_}/{type_}1.json', 'r', encoding='utf-8') as f:
        dishes = json.load(f)

    return [Parser(f'{url}{val}') for val in dishes.values()]
        


def main():
    for j in get_full_info():
        j.set_csv(*j.get_all())


if __name__ == '__main__':
    main()

'https://www.russianfood.com''


# r = requests.get('http://img1.russianfood.com/dycontent/images_upl/459/big_458074.jpg', headers=HEADERS, stream=True)
# with open('img.jpg', 'bw') as f:
#     for chunk in r.iter_content(8192):
#         f.write(chunk)