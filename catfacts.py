import requests,json

def retrieveCatfact(char = 150):
    cat = requests.get(f'https://catfact.ninja/fact?max_length={char}')
    fact = json.loads(cat.text)
    return fact['fact']
