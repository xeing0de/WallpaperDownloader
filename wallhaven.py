import requests
import time
import os
import sys
from menu import *
from bs4 import BeautifulSoup
from tqdm import tqdm

#Get directory
def get_directory():
    while True:
        home_dir = os.environ.get("HOME")
        def_path = os.path.join(home_dir, "Wallpapers")
        path = input('Enter the path to save(Default=\'~/Wallpapers\'): ').strip()
        path = os.path.expanduser(path)
        if path == '' and os.path.isdir('~/Wallpapers'):
            return def_path
        elif not os.path.isdir(path):
            if path == '':
                path = def_path
            os.makedirs(path, exist_ok=True)
        return path

#Delete files in folder
def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

#Last number in folder
def last_file_in_folder(folder_path):
    all_files = os.listdir(folder_path)
    n = len(all_files)
    if(n == 0):
        return 0
    else:
        for i in range(n):
            all_files[i] = int(all_files[i][:-4])
        all_files.sort()
        return all_files[-1]

#Search pages and wallpapers
def pictures(link):
    responce = requests.get(link).text
    soup = BeautifulSoup(responce, 'lxml')
    block = soup.find('main')
    header = block.find('header')
    pages = header.find('h1').text
    int_pictures = int(pages.split(maxsplit=1)[0])
    int_pages = int_pictures // 24 + 1
    return int_pictures, int_pages

#Creating a link
def create_link():
    link = input('Enter wallpaper tags:')

#Enter tags
folder_path = get_directory()
print('Enter wallpaper tags: ', end = '')
name = input()
name = name.replace(' ', '%20').replace('#', '%23')
category = categories()
purit = purity()
ai = ai_filter()
sort = sorting()
rtype, resolutions = resol()

print('Wait...')

#Output the number of wallpapers
link = ("https://wallhaven.cc/search?q=" + name + 
        '&'+ rtype + '=' + resolutions + 
        '&purity=' + purit +
        '&sorting=' + sort +
        '&ai_art_filter=' + ai +
        '&categories=' + category)
print(link)
int_pictures, int_pages = pictures(link)
while(int_pictures == 0):
    print('No such wallpapers, enter other tags:', end = '\n')
    print('Enter wallpaper tags: ', end = '')
    name = input()
    name = name.replace(' ', '%20').replace('#', '%23')
    category = categories()
    purit = purity()
    ai = ai_filter()
    sort = sorting()
    rtype, resolutions = resol()

    print('Wait...')

    #Output the number of wallpapers
    link = ("https://wallhaven.cc/search?q=" + name + 
        '&'+ rtype + '=' + resolutions + 
        '&purity=' + purit +
        '&sorting=' + sort +
        '&ai_art_filter=' + ai +
        '&categories=' + category)
    int_pictures, int_pages = pictures(link)
print('Total pages:', int_pages)
print('Total pictures:', int_pictures)

#Get url of wallpapers
found = []
for i in range(int_pages):
    link = ("https://wallhaven.cc/search?q=" + name + 
        '&'+ rtype + '=' + resolutions + 
        '&purity=' + purit +
        '&sorting=' + sort +
        '&ai_art_filter=' + ai +
        '&categories=' + category +
        '&page=' + str(i+1))
    responce = requests.get(link)
    while(responce.status_code == 429):
        responce = requests.get(link)  
        time.sleep(3)
    soup = BeautifulSoup(responce.text, 'lxml')
    block = soup.find('div', id = "thumbs")
    section = block.find('section')
    li = section.find_all('li')
    for j in li:
        found.append(j.find('a').get('href'))

#Delete old wallpapers
print('Do you want to delete old wallpapers? Y/n(Y):', end = '')
yeah = input()
if yeah == '':
    yeah = 'y'
if yeah in ['N','n', 'no', 'No', 'NO']:
    n = last_file_in_folder(folder_path) + 1
else:
    delete_files_in_folder(folder_path)
    n = 0
    print('Old wallpapers deleted')

#Selecting the number of backgrounds
print('Install all or severall?(All/Num):', end = '')
number = input()
if number == 'A' or number == 'a' or number == 'All' or number == '':
    number = int_pictures
    print('Installing all...')
else:
    print('Installing {} wallpapers...'.format(number))
number = int(number)

#Download wallpapers
for i in tqdm(range(number), desc="Progress", unit="img"):
    responce = requests.get(found[i])
    while(responce.status_code == 429):
        responce = requests.get(found[i])  
        time.sleep(3)
    soup = BeautifulSoup(responce.text, 'lxml')
    block = soup.find('main', id = "main")
    img = block.find('img', id = "wallpaper")
    url_img = img.get('src')
    image_bytes = requests.get(f'{url_img}').content
    with open(f'{folder_path}/{i}.jpg', 'wb') as file:
        file.write(image_bytes)
    with open(f'{folder_path}/{i}.jpg', 'rb') as f:
        pngjpg = f.readline()
    if 'PNG' in str(pngjpg):
        os.remove(folder_path + '/' + str(i) + '.jpg')
        with open(f'{folder_path}/{i}.png', 'wb') as file:
            file.write(image_bytes)
print('\nAll done')
