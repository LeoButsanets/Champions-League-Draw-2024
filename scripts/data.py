from bs4 import BeautifulSoup
import requests

def get_pots():
    # UEFA ranking Web scrapping
    url = 'https://kassiesa.net/uefa/data/method5/trank2023.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    data = soup.find_all('tr', class_ = 'clubline')
    data_adap = [list(filter(None,data[i].getText().split('\n'))) for i in range(36)]

    Teams = []
    for e in data_adap:
        club = e[0] if len(e[0]) > 2 else e[1]
        country = e[1] if len(e[0]) > 2 else e[2]
        Teams.append({'club': club, 'country': country})

    pots = {'A': Teams[0:9], 'B': Teams[9:18], 'C': Teams[18:27], 'D': Teams[27:36]}

    return pots