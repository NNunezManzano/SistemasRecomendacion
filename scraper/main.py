# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from bs4 import BeautifulSoup
import requests

'''


bs_html= requests.get(url_base)
soup = BeautifulSoup(bs_html.text, "html.parser")
'''
url_base = 'https://www.metacritic.com/'

request_session = requests.Session()
request_session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'


endpoint = f'browse/games/score/metascore/year/ps5/filtered?page={numero_pagina}'




game = "resident-evil-4"
cantidad_paginas = 14
for numero_pagina in range(0,cantidad_paginas):
    endpoint = f'game/playstation-5/{game}/user-reviews?page={numero_pagina}'
    html_obtenido = request_session.get(url_base+endpoint)
    soup = BeautifulSoup(html_obtenido.text, "html.parser")

    users = soup.findAll("div", class_ = "review_critic")
    rates = soup.findAll("div", class_ = "review_grade")

    users_dict = {}
    for i in range(0,len(users)):
        users_dict[users[i].div.a.text] = rates[i].div.text

print(users_dict)
