'''
Funciones necsarias para scrapear las reviews de los usuarios dentro de la web https://www.metacritic.com/.

TODO: Agregar comentarios en el codigo
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

    def bestGames(self, page = 0 , all_pages = False):
        
        if all_pages:
            endpoint = f'/browse/games/score/metascore/all/ps4/filtered?page=0'
            html_get = self.request_session.get(self.url_base + endpoint)
            bs_parse = BeautifulSoup(html_get.text, "html.parser")
            paginas = bs_parse.find("li", class_ = "page last_page") 
            cantidad_paginas = int(paginas.a.text)

            game_dict = {}

            for numero_pagina in range(0,cantidad_paginas):
                endpoint = f'/browse/games/score/metascore/all/ps4/filtered?page={numero_pagina}'
                html_get = self.request_session.get(self.url_base + endpoint)
                bs_parse = BeautifulSoup(html_get.text,'html.parser')

                games = bs_parse.findAll("td", class_ = 'clamp-summary-wrap')

                for game in games:
                    game_dict[game.h3.text] = game.find('a', class_='title').get('href')
                
            return game_dict

        endpoint = f'/browse/games/score/metascore/all/ps4/filtered?page={page}'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text,'html.parser')

        games = bs_parse.findAll("td", class_ = 'clamp-summary-wrap')

        game_dict = {}

        for game in games:
            game_dict[game.h3.text] = game.find('a', class_='title').get('href')

        return game_dict
    
    def gameDetails(self, game, endpoint='default', verbose = True):#TODO: agregar nueva funcion que obtenga detalle de los juegos.
        
        if verbose:
            print(f'Juego: {game}')
        
        if endpoint == 'default':
            endpoint = f'/game/{game}/'

        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text, "html.parser")
        nodes = bs_parse.find( 'div',class_ = 'c-productionDetailsGame')

        try:
            imagen = bs_parse.find( 'picture',class_ = 'c-cmsImage').img.get('src')
        except:
            imagen = ''
        try:
            containers = nodes.findAll('div', class_='c-gameDetails_sectionContainer')
            summary = nodes.find('span', class_ = 'c-productionDetailsGame_description').text
        
        except:
             details_dict = {"Sin detalle":game}
             return details_dict

        try:
            rating = nodes.find('div', class_ = 'c-productionDetailsGame_esrb_title').span.text[nodes.find('div', class_ = 'c-productionDetailsGame_esrb_title').span.text.find("Rated")+6:].replace('\n','').replace(' ','')
        
        except:
            print(f'{game} sin rating')
            rating = ''

        i = 0

        for container in containers:

            if i == 0:
                try:
                    platforms_ls = []
                    plataformas = container.find('div', class_='c-gameDetails_Platforms').findAll('li')
                    for plataforma in plataformas:
                        platforms_ls.append(plataforma.text.replace("\n","").replace(" ",""))
                except:
                    platforms_ls = ''
                
                try:
                    release_date = containers[0].find('div', class_='c-gameDetails_ReleaseDate').findAll('span')[1].text
                except:
                    release_date = ''

            if i == 1:
                try:
                    dev_ls = []
                    developers = container.find('div', class_='c-gameDetails_Developer').findAll('ul')
                    for developer in developers:
                        dev_ls.append(developer.text.replace("\n","").replace(" ",""))
                except:
                    dev_ls = ''
                
                try:
                    distribuidor = container.find('div', class_='c-gameDetails_Distributor').findAll('span')[1].text
                except:
                    distribuidor = ''

            if i == 2:
                try:
                    genero = containers[2].a.span.text.replace("\n","").replace(" ","")
                except:
                    genero = ''
            
            if len(containers) < 3:
                genero = ''


            i += 1

        details_dict = {
            'Imagen'        : imagen,
            'Resumen'       : summary,
            'Rating'        : rating,
            'Plataformas'   : platforms_ls,
            'Lanzamiento'   : release_date,
            'Developer(s)'  : dev_ls,
            'Distribuidor'  : distribuidor,
            'Genero'        : genero
        }

        return details_dict
            


    def usersReviews(self, users_dict:dict, game:str, endpoint:str, verbose = True):
        
        if verbose:
            print(f"Juego: {game}")
        
        endpoint = f'{endpoint}/user-reviews?page=0'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text, "html.parser")
        paginas = bs_parse.find("li", class_ = "page last_page") 

        cantidad_paginas = 0

        if paginas != None:
            cantidad_paginas = int(paginas.a.text)

        random_sleep = 99

        if cantidad_paginas > 5 and cantidad_paginas != 0:

            random_sleep = random.randint(5, cantidad_paginas)
        
        if cantidad_paginas > 50:

            cantidad_paginas = 50
        
        for numero_pagina in range(0,cantidad_paginas):

            if verbose:
                print(f"Pagina {numero_pagina+1}/{cantidad_paginas}")
            
            endpoint = f'{endpoint}/user-reviews?page={numero_pagina}'
            html_get = self.request_session.get(self.url_base+endpoint)
            bs_parse = BeautifulSoup(html_get.text, "html.parser")

            users = bs_parse.findAll("div", class_ = "review_critic")
            rates = bs_parse.findAll("div", class_ = "review_grade")

            for i in range(0,len(users)):
                try:
                    user = users[i].a.text
                except:    
                    user = users[i].div.text
                
                rate = rates[i].div.text

                if user in users_dict.keys():
                    users_dict[user][game] = rate

                else:
                    users_dict[user] = {game:rate} 
                    
            
            
            if numero_pagina%random_sleep == 0 and numero_pagina != 0:
                time.sleep(random.randint(30, 60))    
            
            time.sleep(random.randint(1, 10))

        return users_dict
    
    def allReviews(self, user:str):
        endpoint = f'/user/{user}'
        html_get = self.request_session.get(self.url_base + endpoint)
        bs_parse = BeautifulSoup(html_get.text, "html.parser")
        allreviews = bs_parse.findAll("div", class_="review_section review_data") 
        
        reviews_dict = {}
        endpoint_dict ={}
        
        for review in allreviews:
            if 'playstation-4' in review.find("div", class_="product_title").a.get("href"):
                game_name = review.find("div", class_="product_title").text
                game = self.gameName(game_name)
                rating = review.find("div", class_="review_score").div.text
                endpoint = review.find("div", class_="product_title").a.get("href")
                reviews_dict[game] = rating
                endpoint_dict[game] = endpoint
        
        return reviews_dict, endpoint_dict

    def gameName(self,game):

        if ":" in game:
            game = game.replace(":", "")

        game = game.replace(" ", "-").lower()

        return game
    

