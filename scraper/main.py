'''

TODO: Agregar comentarios en el codigo
'''

import json
from scraper import GameScraper
import scraper_api as scapi

import os
import time
import random

url = 'https://www.metacritic.com'

gs = GameScraper(url)

bg_dict = gs.bestGames()#puedo pasar numero de pagina como argumento (page=#)

def get_reviews(bg_dict:dict):
    if not os.path.exists('./reviews.json'):
        game_dict = {}

    else:
        with open('./reviews.json', 'r') as json_reviews:
            game_dict = json.load(json_reviews)

    if os.path.exists('./r_scraped.txt'):
        with open('./r_scraped.txt', 'r') as scraped_txt:
            games_ls = scraped_txt.readlines()
            last_scraped = games_ls[-1].replace("\n","")

            games_to_scrape = {}

            scrape_games = False

            for game_name, url in bg_dict.items():

                game = gs.gameName(game_name)

                if scrape_games:
                    games_to_scrape[game] = url

                if game == last_scraped:

                    scrape_games = True

            bg_dict = games_to_scrape

    else:
        with open('./r_scraped.txt', 'w') as scraped_txt:
            scraped_txt.writelines(('Lista de juegos\n'))



    for (game_name,endpoint) in bg_dict.items():
        
        game = gs.gameName(game_name)
        game_dict = gs.usersReviews(game_dict,game,endpoint)

        
        with open('./reviews.json', 'w') as json_reviews:
            
            json.dump(game_dict, json_reviews, indent=4)

        with open('./r_scraped.txt', 'a') as scraped_txt:
            scraped_txt.writelines((str(game)+'\n'))

def get_details(bg_dict:dict, verbose = True):
    
    if not os.path.exists('./game_details.json'):
        game_dict = {}

    else:
        with open('./game_details.json', 'r') as json_reviews:
            game_dict = json.load(json_reviews)

    if os.path.exists('./gd_scraped.txt'):
        with open('./gd_scraped.txt', 'r') as scraped_txt:
            games_ls = scraped_txt.readlines()
            last_scraped = games_ls[-1].replace("\n","")

            games_to_scrape = {}

            scrape_games = False

            for game, url in bg_dict.items():

                #game = gs.gameName(game_name)

                if scrape_games:
                    games_to_scrape[game] = url

                if game == last_scraped:

                    scrape_games = True

            bg_dict = games_to_scrape

    else:
        with open('./gd_scraped.txt', 'w') as scraped_txt:
            scraped_txt.writelines(('Lista de juegos\n'))

    game_list = list(bg_dict.keys())

    cantidad_juegos = len(game_list)

    g = 1
    
    for (game,endpoint) in bg_dict.items():

        if verbose:
            print(f'{game} - {g}/{cantidad_juegos}')
            g += 1
        
        #game = gs.gameName(game_name)
        details_dict = gs.gameDetails(game,endpoint, verbose=False) 

        try:
            sin_detalle = details_dict['Sin detalle'] 
            with open('./gd_scraped.txt', 'a') as scraped_txt:
                scraped_txt.writelines(('Sin detalle' + str(sin_detalle) + '\n'))
        
        except:
            game_dict[game] = details_dict

            with open('./game_details.json', 'w') as json_reviews:
            
                json.dump(game_dict, json_reviews, indent=4)

            with open('./gd_scraped.txt', 'a') as scraped_txt:
                scraped_txt.writelines((str(game)+'\n'))
        
        
        time.sleep(random.randint(1, 10))
    

    

def get_allReviews(verbose = True): 
    if not os.path.exists('./reviews.json'):
        return "No hay usuarios para buscar."        

    else:
        with open('./reviews.json', 'r') as json_reviews:
            
            users_dict = json.load(json_reviews)
            users_list = list(users_dict.keys())    

    if os.path.exists('./u_scraped.txt'):
        with open('./u_scraped.txt', 'r') as scraped_txt:
            
            users_ls = scraped_txt.readlines()
            last_scraped = users_ls[-1].replace("\n","")

            users_to_scrape = []

            scrape_user = False

            for user in users_list:

                if scrape_user:
                    users_to_scrape.append(user)

                if user == last_scraped:

                    scrape_user = True

            users_list = users_to_scrape

    else:
        with open('./u_scraped.txt', 'w') as scraped_txt:
            scraped_txt.writelines(('Usuarios scrapeados\n'))

    with open('./gd_scraped.txt', 'r') as details_txt:
        rawdetails_ls = details_txt.readlines()
        details_ls = []

        for detail in rawdetails_ls:
            details_ls.append(detail.replace("\n",""))


    pending_details = {}

    cantidad_total = len(users_list)

    i = 1

    for user in users_list:
        
        if verbose:
            print(f'{user} - {i}/{cantidad_total}' )
        
        i += 1

        json_api = scapi.allReviewsAPI(user)
        
        user_reviews,game_endpoint = scapi.allReviews(json_api, details_ls)
        
        if user_reviews != {}:
            for game, review in user_reviews.items():
                users_dict[user][game] = str(review)
        
            for game, endpoint in game_endpoint.items():
                if game not in details_ls:
            
                    if verbose:
                        print(game)

                    pending_details[game] = endpoint
        
            with open('./reviews.json', 'w') as json_reviews:
                json.dump(users_dict, json_reviews, indent=4)

            with open('./u_scraped.txt', 'a') as scraped_txt:
                scraped_txt.writelines((str(user)+'\n'))
        
            with open('./pending_details.json', 'w') as pending_details_json:
                json.dump(pending_details, pending_details_json, indent=4)
        
        time.sleep(random.randint(2,7))


if __name__ == '__main__':
    with open('./pending_details.json', 'r') as pend_details:
            bg_dict = json.load(pend_details)
    get_details(bg_dict)