import json
import pandas as pd
import os
import numpy as np
from glob import glob
from datetime import datetime

# Toma todos los .json de la carpeta actual
JSON_FILES = ["top.json", "jungler.json", "mid.json","adc.json", "support.json"]

BASE_COLUMNS = [
    "name_es",
    "win_rate_percent",
    "appear_rate_percent",
    "forbid_rate_percent",
    "difficultyL",
]

date = datetime.now().strftime("%Y-%m-%d")
output_file = f"{date}.xlsx"

def json_to_dataframe(path: str) -> pd.DataFrame:
    """Carga el json y devuelve un DataFrame con las columnas bases
    más el percentil del Winrate, Pickrate y Banrate, el ranking final (parámetro del orden) y el tier correspondiente.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        rows.append({
            "name_es": item.get("name_es"),
            "win_rate_percent": float(item.get("win_rate_percent", 0)),
            "appear_rate_percent": float(item.get("appear_rate_percent", 0)),
            "forbid_rate_percent": float(item.get("forbid_rate_percent", 0)),
            "difficultyL": float(item.get("difficultyL", 0)),
        })

    df = pd.DataFrame(rows, columns=BASE_COLUMNS)

    # PERCENTIL WINRATE
    w = df["win_rate_percent"]
    ranks = w.rank(method="min", ascending=True)

    n = len(df)
    if n > 1:
        df["ranking_winrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_winrate"] = 0.0

    # PERCENTIL PICKRATE
    p = df["appear_rate_percent"]
    ranks = p.rank(method="min", ascending=True)

    n = len(df)
    if n > 1:
        df["ranking_pickrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_pickrate"] = 0.0

    # PERCENTIL BANRATE
    b = df["forbid_rate_percent"]
    ranks = b.rank(method="min", ascending=True)

    n = len(df)
    if n > 1:
        df["ranking_banrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_banrate"] = 0.0

    # RANKING FINAL PONDERADO
    df["ranking_final"] = ((
        (df["ranking_winrate"] * 0.60
        + df["ranking_pickrate"] * 0.32
        + df["ranking_banrate"] * 0.08)
        * 1 - ((df["difficultyL"] - 1) * 0.2)).round(2)
    )

    # CHAMPTIER
    conditions = [
    (df["ranking_final"] >= 85),
    (df["ranking_final"] >= 70),
    (df["ranking_final"] >= 45),
    (df["ranking_final"] >= 20),
    (df["ranking_final"] >= 0)
    ]

    choices = ["S+", "S", "A", "B", "C"]

    df["champ_tier"] = np.select(conditions, choices, default="")


    # ORDENAMIENTO POR RANKING FINAL PONDERADO
    df = df.sort_values(by="ranking_final", ascending=False).reset_index(drop=True)

    return df

def main():
    if not JSON_FILES:
        print("No se encontraron archivos JSON en la carpeta actual.")
        return

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for path in JSON_FILES:
            df = json_to_dataframe(path)

            # Nombre de la pestaña = nombre del archivo sin extensión
            sheet_name = os.path.splitext(os.path.basename(path))[0][:31]

            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Ajustar ancho de las columnas del Excel
            sheet = writer.sheets[sheet_name]
            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        value = str(cell.value)
                        if value is not None:
                            max_length = max(max_length, len(value))
                    except:
                        pass

                sheet.column_dimensions[column].width = max_length + 4

    print(f"Estadísticas obtenidas: {output_file}")

if __name__ == "__main__":
    main()
