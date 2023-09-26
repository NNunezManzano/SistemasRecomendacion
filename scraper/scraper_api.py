"""
Funciones necesarias para scrapear a traves de la API del sitio
TODO: Agregar comentarios en el codigo
"""
from scraper import GameScraper

import requests
import json

def allReviews(response:json, details:list):
    
    gs = GameScraper("url")

    data =  response.json()

    items = data['data']['items']

    reviews_dict = {}
    endpoint_dict ={}

    for item in items:
        if item['platform'] == "PlayStation 4":
            game_name = item['reviewedProduct']['title']
            game = gs.gameName(game_name)

            if game not in details:
                rating = item['score']

                endpoint = item['reviewedProduct']['url']

                reviews_dict[game] = rating
                endpoint_dict[game] = endpoint
    
    return reviews_dict, endpoint_dict


def allReviewsAPI(user):

    request_session = requests.Session()
    request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
    request_session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    request_session.headers['Accept-Encoding'] = 'gzip, deflate, br'
    request_session.headers['Accept-Lenguaje'] = 'en-US,en;q=0.9'
    
    # Define the API endpoint URL
    url = f"https://fandom-prod.apigee.net/v1/xapi/reviews/metacritic/user/users/{user}/web"

    # Define the payload parameters
    payload = {
        "apiKey": "1MOZgmNFxvmljaQR1X9KAij9Mo4xAY3u",
        "componentName": "profile",
        "componentDisplayName": "Profile",
        "componentType": "Profile",
        "filterByType": "games"
    }

    # Make the GET request
    response = request_session.get(url, params=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        return response

    else:
        # If the request was not successful, print an error message
        print(f"Error: {response.status_code} - {response.text}")

#TODO: agregar nueva funcion que obtenga detalle de los juegos.
'''
# GAMES DETAILS
# Devuelve nombre del juego y detalles en formato dict
"red-dead-redemption-2": {
        "Rating": [
            "M"
        ],
        "Developer": [
            "RockstarGames"
        ],
        "Genre(s)": [
            "ActionAdventure",
            "Open-World"
        ],
        "Number of Online Players": [
            "Upto32Players"
        ]
    },

url = f"https://www.metacritic.com/game/hitman-definitive-edition/"
html_raw = request_session.get(url)
bs_parse = BeautifulSoup(html_raw.text, "html.parser")
nodes = bs_parse.find( 'div',class_ = 'c-productionDetailsGame')

containers = nodes.findAll('div', class_='c-gameDetails_sectionContainer')

containers[2].a.span.text


i = 0

for container in containers:
    
    if i == 0:
        platforms_ls = []
        plataformas = container.find('div', class_='c-gameDetails_Platforms').findAll('li')
        for plataforma in plataformas:
            platforms_ls.append(plataforma.text.replace("\n","").replace(" ",""))

        release_date = containers[0].find('div', class_='c-gameDetails_ReleaseDate').findAll('span')[1].text
    
    if i == 1:
        
        dev_ls = []
        developers = container.find('div', class_='c-gameDetails_Developer').findAll('ul')
        for developer in developers:
            dev_ls.append(developer.text.replace("\n","").replace(" ",""))

        distribuidor = container.find('div', class_='c-gameDetails_Distributor').findAll('span')[1].text

    if i == 2:
        genero = containers[2].a.span.text.replace("\n","").replace(" ","")
'''