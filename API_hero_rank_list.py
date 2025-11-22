import requests
import json

URL = "https://mlol.qt.qq.com/go/lgame_battle_info/hero_rank_list_v2"

def main():
    # Hacemos la request a la API
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()   # Si hay error, que explote

    data = resp.json()  # Convertimos a JSON

    # Guardamos el JSON con formato bonito
    with open("data_hero_rank.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))

    print("Datos guardados en data_hero_rank.txt")

if __name__ == "__main__":
    main()
