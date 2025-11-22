import requests
import json

URL = "https://game.gtimg.cn/images/lgamem/act/lrlib/js/heroList/hero_list.js"

def main():
    # Hacemos la request a la API
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()   # Si hay error, que explote

    data = resp.json()  # Convertimos a JSON
    list_data = []
    for item in data['heroList']:
        champ_name = (data['heroList'][item]['name'])
        list_data.append(champ_name)

    # Guardamos el JSON con formato bonito
    with open("data_name_hero.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(list_data, ensure_ascii=False, indent=2))

    print("Datos guardados en data_hero.txt")

if __name__ == "__main__":
    main()
