import requests
from bs4 import BeautifulSoup

def fetch_headlines():
    url = "https://news.ycombinator.com/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = soup.find_all('a', class_='titleline')

        if headlines:
            for link in headlines:
                print(link.get('href'))
        else:
            print('No titleline found on this page')
        
    except requests.exceptions.RequestException as e:
        print(f"A network error occured {e}")


if __name__ == '__main__':
    fetch_headlines()