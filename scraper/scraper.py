#

from bs4 import BeautifulSoup
import requests
import random
import time

class GameScraper():
    def __init__(self, url):
        self.url_base = url
        self.request_session = requests.Session()
        self.request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'

    def bestGames(self):

        endpoint = f'browse/games/score/metascore/year/ps5/filtered?page=0'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text,'html.parser')

        games = bs_parse.findAll("td", class_ = 'clamp-summary-wrap')

        game_list = []

        for game in games:
            game_list.append(game.h3.text)

        return game_list

    def usersReviews(self, game):
        '''
        endpoint = f'game/playstation-5/{game}/user-reviews?page=0'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text, "html.parser")
        paginas = bs_parse.find("li", class_ = "page last_page") #Por algún motivo a veces funciona y a veces no

        cantidad_paginas = paginas.a.text

        print(cantidad_paginas)
        '''
        users_dict = {}

        for numero_pagina in range(0,1):# for numero_pagina in range(0,cantidad_paginas):
            time.sleep(random.randint(10, 120))

            endpoint = f'game/playstation-5/{game}/user-reviews?page={0}'#endpoint = f'game/playstation-5/{game}/user-reviews?page={cantidad_paginas}'
            html_get = self.request_session.get(self.url_base+endpoint)
            bs_parse = BeautifulSoup(html_get.text, "html.parser")

            users = bs_parse.findAll("div", class_ = "review_critic")
            rates = bs_parse.findAll("div", class_ = "review_grade")

            for i in range(0,len(users)):
                users_dict[users[i].div.a.text] = rates[i].div.text

        return users_dict

    def gameName(self,game):

        if ":" in game:
            game = game.replace(":", "")

        game = game.replace(" ", "-").lower()

        return game
