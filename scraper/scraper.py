'''
Funciones necsarias para scrapear las reviews de los usuarios dentro de la web https://www.metacritic.com/.

'''

from bs4 import BeautifulSoup
import requests
import random
import time

class GameScraper():
    def __init__(self, url):
        self.url_base = url
        self.request_session = requests.Session()
        self.request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
        self.request_session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        self.request_session.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.request_session.headers['Accept-Lenguaje'] = 'en-US,en;q=0.9'

    def bestGames(self, page = 0):
        #TODO: Extraer URL de cada juego

        endpoint = f'browse/games/score/metascore/all/ps4/filtered?page={page}'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text,'html.parser')

        games = bs_parse.findAll("td", class_ = 'clamp-summary-wrap')

        game_list = []

        for game in games:
            game_list.append(game.h3.text)

        return game_list

    def usersReviews(self, game, verbose = True):#TODO: Modificar para recibir URL del juego
        
        if verbose:
            print(f"Juego: {game}")
        
        endpoint = f'game/playstation-4/{game}/user-reviews?page=0'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text, "html.parser")
        paginas = bs_parse.find("li", class_ = "page last_page") 

        cantidad_paginas = int(paginas.a.text)

        users_dict = {}

        random_sleep = random.randint(5, cantidad_paginas)

        for numero_pagina in range(0,3):
            
            if verbose:
                print(f"Pagina {numero_pagina+1}/{cantidad_paginas}")
            
            endpoint = f'game/playstation-4/{game}/user-reviews?page={numero_pagina}'
            html_get = self.request_session.get(self.url_base+endpoint)
            bs_parse = BeautifulSoup(html_get.text, "html.parser")

            users = bs_parse.findAll("div", class_ = "review_critic")
            rates = bs_parse.findAll("div", class_ = "review_grade")

            for i in range(0,len(users)):
                try:
                    users_dict[users[i].a.text] = rates[i].div.text #TODO: Modificar dict para que pase {Usuario:{juego:rating}}
                except:
                     users_dict[users[i].div.text] = rates[i].div.text
            
            if numero_pagina%random_sleep == 0:
                time.sleep(random.randint(11, 60))    
            
            time.sleep(random.randint(1, 10))

        return users_dict

    def gameName(self,game):

        if ":" in game:
            game = game.replace(":", "")

        game = game.replace(" ", "-").lower()

        return game
