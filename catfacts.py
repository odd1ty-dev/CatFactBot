import requests,json
from time import sleep

def retrieveCatfact(char = 150):
    cat = requests.get(f'https://catfact.ninja/fact?max_length={char}')
    sleep(1)
    fact = json.loads(cat.text)
    return fact['fact']

if __name__=='__main__':
    print(retrieveCatfact())