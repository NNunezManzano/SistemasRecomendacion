'''


'''

import json
from scraper import GameScraper
import os

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

def get_details(bg_dict:dict):
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

            for game_name, url in bg_dict.items():

                game = gs.gameName(game_name)

                if scrape_games:
                    games_to_scrape[game] = url

                if game == last_scraped:

                    scrape_games = True

            bg_dict = games_to_scrape

    else:
        with open('./gd_scraped.txt', 'w') as scraped_txt:
            scraped_txt.writelines(('Lista de juegos\n'))



    for (game_name,endpoint) in bg_dict.items():
        
        game = gs.gameName(game_name)
        details_dict = gs.gameDetails(game,endpoint)

        game_dict[game] = details_dict
        
        with open('./game_details.json', 'w') as json_reviews:
            
            json.dump(game_dict, json_reviews, indent=4)

        with open('./gd_scraped.txt', 'a') as scraped_txt:
            scraped_txt.writelines((str(game)+'\n'))
