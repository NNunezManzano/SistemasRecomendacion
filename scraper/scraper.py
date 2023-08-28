# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from bs4 import BeautifulSoup
import requests

'''
'https://www.metacritic.com/'
game = "resident-evil-4"
'''
class GameScraper():
    def __init__(self, url):
        self.url_base = url
        self.request_session = requests.Session()
        self.request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'

    def bestGames(self):

        endpoint = f'browse/games/score/metascore/year/ps5/filtered?page=0'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text,'html.parser')

        games = bs_parse.find("td", class_ = 'clamp-summary-wrap')

        return games.a.h3.text

    def usersReviews(self, game):

        users_dict = {}
        cantidad_paginas = 14

        for numero_pagina in range(0,cantidad_paginas):

            endpoint = f'game/playstation-5/{game}/user-reviews?page={numero_pagina}'
            html_get = self.request_session.get(self.url_base+endpoint)
            bs_parse = BeautifulSoup(html_get.text, "html.parser")

            users = bs_parse.findAll("div", class_ = "review_critic")
            rates = bs_parse.findAll("div", class_ = "review_grade")

            users_dict = {}

            for i in range(0,len(users)):
                users_dict[users[i].div.a.text] = rates[i].div.text

        return users_dict
