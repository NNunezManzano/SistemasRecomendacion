'''
game = "resident-evil-4"

'''

import json
from scraper import GameScraper
import os
'''
Ejemplo de funcionamiento del logueo
lista = ["1","2","3"]


if not os.path.exists('./scrapeados.txt'):
    with open('./scrapeados.txt', 'w') as scrapeados:
        scrapeados.writelines((str(i)+'\n' for i in lista))
else:
    with open('./scrapeados.txt', 'r') as scrapeados:
        # Reading from file
        x = scrapeados.readlines()
        print(x[-1].replace("\n",""))
        # Closing file
        scrapeados.close()
'''

#TODO: Agregar Logueo al loop
#Va a consisitir de dos archivos: 
# - Un txt donde cada vez que termine de scrapear un juego guarde el nombre
# - Un json donde cada vez que termine de scrapear un juego guarde el dict

url = 'https://www.metacritic.com/'

gs = GameScraper(url)

bg_list = gs.bestGames()#puedo pasar numero de pagina como argumento (page=#)

game_dict = {}
for i in ([0,1]):
    game_name = gs.gameName(bg_list[i])
    game_dict[game_name] = gs.usersReviews(game_name)
    with open('./reviews.json', 'a') as f:
        json_string = json.dumps(game_dict)
        f.write(json_string)


    



'''
from bs4 import BeautifulSoup
import requests

request_session = requests.Session()
request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
request_session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
request_session.headers['Accept-Encoding'] = 'gzip, deflate, br'
request_session.headers['Accept-Lenguaje'] = 'en-US,en;q=0.9'

url = 'https://www.whatismybrowser.com/'\
 'developers/what-http-headers-is-my-browser-sending'
req = request_session.get(url)
bs = BeautifulSoup(req.text, 'html.parser')
print(bs.find('table', {'class':'table-striped'}).get_text)



url = 'https://www.metacritic.com/'
endpoint = f'game/playstation-4/red-dead-redemption-2/user-reviews?page=0'#endpoint = f'game/playstation-5/{game}/user-reviews?page={cantidad_paginas}'
html_get = request_session.get(url+endpoint)
bs_parse = BeautifulSoup(html_get.text, "html.parser")
users_dict = {}
users = bs_parse.findAll("div", class_ = "review_critic")
rates = bs_parse.findAll("div", class_ = "review_grade")
print(rates[100].div.text)
print(rates[101].div.text)


'''



