import requests

name_heros = ['Hulk', 'Captain America', 'Thanos']
info_heros = []
try:
    res = requests.get("https://akabab.github.io/superhero-api/api/all.json")
    data = res.json()
    for item in data:
        if item['name'] in name_heros:
            info_heros.append(item)
    fin_max = max(info_heros, key=lambda x: x['powerstats']['intelligence'])
    print(fin_max) # все данные о герое с высоким интеллектом
except Exception as e:
    print("Exception:", e)
