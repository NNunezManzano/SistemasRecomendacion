'''

game = "resident-evil-4"

'''
from scraper import GameScraper

url = 'https://www.metacritic.com/'

gs = GameScraper(url)

bg_list = gs.bestGames()

game_dict = {}
for i in ([0,1]):
    game_name = gs.gameName(bg_list[i])
    game_dict[game_name] = gs.usersReviews(game_name)

print(game_dict)



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


'''



