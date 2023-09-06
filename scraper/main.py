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

url = 'https://www.metacritic.com'

gs = GameScraper(url)

bg_dict = gs.bestGames()#puedo pasar numero de pagina como argumento (page=#)

if not os.path.exists('./reviews.json'):
    game_dict = {}

else:
    with open('./reviews.json', 'r') as json_reviews:
        game_dict = json.load(json_reviews)

if os.path.exists('./scraped.txt'):
    with open('./scraped.txt', 'r') as scraped_txt:
        games_ls = scraped_txt.readlines()
        last_scraped = games_ls[-1].replace("\n","")
else:
    with open('./scraped.txt', 'w') as scraped_txt:
        scraped_txt.writelines(('Lista de juegos\n'))


for (game_name,endpoint) in zip(bg_dict.keys(),bg_dict.values()):
    #TODO: Agregar logica para iniciar desde el ultimo scrapeado    
    game = gs.gameName(game_name)
    game_dict = gs.usersReviews(game_dict,game,endpoint)

    # Open the same JSON file for writing (overwrite)
    with open('./reviews.json', 'w') as json_reviews:
        # Write the updated dictionary back to the JSON file
        json.dump(game_dict, json_reviews, indent=4)

    with open('./scraped.txt', 'a') as scraped_txt:
        scraped_txt.writelines((str(game)+'\n'))
    


    

    



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


#REVIEWS
url = 'https://www.metacritic.com/'
endpoint = f'game/playstation-4/red-dead-redemption-2/user-reviews?page=0'#endpoint = f'game/playstation-5/{game}/user-reviews?page={cantidad_paginas}'
html_get = request_session.get(url+endpoint)
bs_parse = BeautifulSoup(html_get.text, "html.parser")
users_dict = {}
users = bs_parse.findAll("div", class_ = "review_critic")
rates = bs_parse.findAll("div", class_ = "review_grade")
print(rates[100].div.text)
print(rates[101].div.text)



#BEST GAMES
url = 'https://www.metacritic.com/'
endpoint = 'browse/games/score/metascore/all/ps4/filtered?page=0'


html_get = request_session.get(url + endpoint)
bs_parse = BeautifulSoup(html_get.text,'html.parser')

games = bs_parse.findAll("td", class_ = 'clamp-summary-wrap')

print(games[0].find('a', class_='title').get('href'))
'''


