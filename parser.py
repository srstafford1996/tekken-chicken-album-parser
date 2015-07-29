import csv
import os
import urllib.request as request
import json
from bs4 import BeautifulSoup



def getLinks():

    characters = []
    with open('spreadsheet.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:

            if row[5] == 'Y':

                characters.append( {'name': row[0], 'link' : row[6]} );

    return characters



def downloadAlbum(name, url):

    html = request.urlopen(url + '/layout/blog').read().decode('utf-8')
    parsed = BeautifulSoup(html, 'html.parser')

    images = []

    #Find the images in the thumbs-top list
    imgtags = parsed.find('div', {'id': 'thumbs-top'}).find_all('img')

    for img in imgtags:
        img_id = img['id'].replace('thumb-', '')
        url = 'i.imgur.com/' + img_id + '.gif'
        images.append({'notation': img['title'], 'url': url})

    imgtags = parsed.find('div', {'id': 'thumbs-bottom'}).find_all('img')

    for img in imgtags:
        img_id = img['id'].replace('thumb-', '')
        url = 'http://i.imgur.com/' + img_id + '.gif'
        images.append({'notation': img['title'], 'url': url});

    i = 1

    img_map = {}

    for image in images:
        print('Downloading ' + name + ' ' + image['notation'] + ' from ' + image['url'])

        #Map attack to image file
        img_map[image['notation']] = str(i) + '.gif'

        #Download image file
        try:
            request.urlretrieve(url, os.path.join(os.getcwd(), 'gifs', name , str(i) + '.gif' ))
        except FileNotFoundError:
            #Make directory
            os.makedirs(os.path.join(os.getcwd(), 'gifs', name))
            request.urlretrieve(url, os.path.join(os.getcwd(), 'gifs', name , str(i) + '.gif' ))

        i += 1

    #Map image files to notation
    filename = os.path.join(os.getcwd(), 'gifs', name, 'map.json' )
    with open(filename, 'w') as f:
        json.dump(img_map, f, sort_keys = True, indent = 4, separators = (',', ': '))


characters = getLinks();


print('\nSELECT CHARACTER TO DOWNLOAD.\nPRESS 0 TO DOWNLOAD ALL\n\n')

inp = -2
while(inp != -1):

    i = 1
    for character in characters:
        print(str(i) + ': ' + character['name'])
        i += 1


    inp = int(input())

    if inp == 0:
        for character in characters:
            downloadAlbum(character['name'], character['link'])
    elif inp != -1 and inp <= len(characters):
        downloadAlbum(characters[inp-1]['name'], characters[inp-1]['link'])
