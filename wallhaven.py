import requests
import time
import os
import sys
from bs4 import BeautifulSoup

#Get directory
def get_directory():
    while True:
        home_dir = os.environ.get("HOME")
        def_path = os.path.join(home_dir, "Wallpapers")
        path = input('Enter the path to save(Default=\'~/Wallpapers\'): ').strip()
        path = os.path.expanduser(path)
        if path == '' and os.path.isdir('~/Wallpapers'):
            print(1)
            return def_path
        elif not os.path.isdir(path):
            if path == '':
                print(2)
                path = def_path
            print(3)
            os.makedirs(path, exist_ok=True)
        return path

#Delete files in folder
def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')

#Функция поиска последнего номера фона
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

#Функция поиска страниц и фонов
def pictures(link):
    responce = requests.get(link).text
    soup = BeautifulSoup(responce, 'lxml')
    block = soup.find('main')
    header = block.find('header')
    pages = header.find('h1').text
    int_pictures = int(pages.split(maxsplit=1)[0])
    int_pages = int_pictures // 24 + 1
    return int_pictures, int_pages

#Ввод тегов и количество фонов
folder_path = get_directory()
print('Enter wallpaper tags: ', end = '')
name = input()
name = name.replace(' ', '%20')
name = name.replace('#', '%23')
print('Enter resolutions(1920x1080): ', end = '')
resolutions = input()
print('Wait...')
if resolutions == '':
    resolutions = '1920x1080'
resolutions = resolutions.replace(' ', '%2C')

#Вывод количества страниц
link = "https://wallhaven.cc/search?q=" + name + '&resolutions='+ resolutions + '&purity=110&sorting=views'
int_pictures, int_pages = pictures(link)
while(int_pictures == 0):
    print('No such wallpapers, enter other tags:', end = '')
    name = input()
    name = name.replace(' ', '%20')
    name = name.replace('#', '%23')
    print('Enter resolutions(1920x1080): ', end = '')
    resolutions = input()
    if resolutions == '':
        resolutions = '1920x1080'
    resolutions = resolutions.replace(' ', '%2C')
    link = "https://wallhaven.cc/search?q=" + name + '&resolutions='+ resolutions + '&purity=110&sorting=views'
    int_pictures, int_pages = pictures(link)
    print('Wait...')
print('Total pages:', int_pages)
print('Total pictures:', int_pictures)

#Поиск ссылок фонов
found = []
for i in range(int_pages):
    link = "https://wallhaven.cc/search?q=" + name + '&resolutions='+ resolutions + '&purity=110&sorting=views' + '&page=' + str(i + 1)
    responce = requests.get(link)
    while(responce.status_code == 429):
        responce = requests.get(link)  
    soup = BeautifulSoup(responce.text, 'lxml')
    block = soup.find('div', id = "thumbs")
    section = block.find('section')
    li = section.find_all('li')
    for j in li:
        found.append(j.find('a').get('href'))

#Удаление фонов
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

#Выбор количесвта устанавливаемых фонов
print('Install all or severall?(All/Num):', end = '')
number = input()
if number == 'A' or number == 'a' or number == 'All' or number == '':
    number = int_pictures
    print('Installing all...')
else:
    print('Installing {} wallpapers...'.format(number))
number = int(number)

#Скачивание фонов
for i in range(number):
    responce = requests.get(found[i])
    while(responce.status_code == 429):
        responce = requests.get(found[i])  
    soup = BeautifulSoup(responce.text, 'lxml')
    block = soup.find('main', id = "main")
    img = block.find('img', id = "wallpaper")
    url_img = img.get('src')
    image_bytes = requests.get(f'{url_img}').content
    with open(f'{folder_path}/{n}.jpg', 'wb') as file:
        file.write(image_bytes)
    with open(f'{folder_path}/{n}.jpg', 'rb') as f:
        pngjpg = f.readline()
    if 'PNG' in str(pngjpg):
        os.remove(folder_path + '/' + str(n) + '.jpg')
        with open(f'{folder_path}/{n}.png', 'wb') as file:
            file.write(image_bytes)
    n = n + 1
    sys.stdout.write("\rDownloading {}...".format(i+1))
    sys.stdout.flush()
print('\nAll done')
