import json
import pandas as pd
import os
from glob import glob


# Toma todos los .json de la carpeta actual
JSON_FILES = ["top.json", "jungler.json", "mid.json","adc.json", "support.json"]

OUTPUT_FILE = "estadisticas_heroes.xlsx"

BASE_COLUMNS = [
    "name_es",
    "avatar",
    "win_rate_percent",
    "appear_rate_percent",
    "forbid_rate_percent",
    "difficultyL",
]

def json_to_dataframe(path: str) -> pd.DataFrame:
    """Carga un JSON y devuelve un DataFrame con las columnas deseadas
    + la columna ranking_pct calculada en base a win_rate_percent.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        rows.append({
            "name_es": item.get("name_es"),
            "avatar": item.get("avatar"),
            "win_rate_percent": float(item.get("win_rate_percent", 0)),
            "appear_rate_percent": float(item.get("appear_rate_percent", 0)),
            "forbid_rate_percent": float(item.get("forbid_rate_percent", 0)),
            "difficultyL": float(item.get("difficultyL", 0)),
        })

    df = pd.DataFrame(rows, columns=BASE_COLUMNS)

    # ---- Cálculo equivalente a tu fórmula de Excel ----
    # JERARQUIA(...; rango; 1) = rank ascendente (1 = menor valor)
    w = df["win_rate_percent"]
    ranks = w.rank(method="min", ascending=True)  # como JERARQUIA(...;...;1)

    n = len(df)
    if n > 1:
        df["ranking_winrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_winrate"] = 0.0
    # ---------------------------------------------------

        # ---- Cálculo equivalente a tu fórmula de Excel ----
    # JERARQUIA(...; rango; 1) = rank ascendente (1 = menor valor)
    p = df["appear_rate_percent"]
    ranks = p.rank(method="min", ascending=True)  # como JERARQUIA(...;...;1)

    n = len(df)
    if n > 1:
        df["ranking_pickrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_pickrate"] = 0.0
    # ---------------------------------------------------

        # ---- Cálculo equivalente a tu fórmula de Excel ----
    # JERARQUIA(...; rango; 1) = rank ascendente (1 = menor valor)
    b = df["forbid_rate_percent"]
    ranks = b.rank(method="min", ascending=True)  # como JERARQUIA(...;...;1)

    n = len(df)
    if n > 1:
        df["ranking_banrate"] = ((ranks - 1) / (n - 1) * 100).round(2)
    else:
        df["ranking_banrate"] = 0.0
    # ---------------------------------------------------

        # ---- Score final ponderado ----
    df["ranking_final"] = ((
        (df["ranking_winrate"] * 0.60
        + df["ranking_pickrate"] * 0.32
        + df["ranking_banrate"] * 0.08)
        * 1 - ((df["difficultyL"] - 1) * 0.2)).round(2)

    )
    # -------------------------------

    return df

def main():
    if not JSON_FILES:
        print("No se encontraron archivos JSON en la carpeta actual.")
        return

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        for path in JSON_FILES:
            df = json_to_dataframe(path)

            # Nombre de la pestaña = nombre del archivo sin extensión
            sheet_name = os.path.splitext(os.path.basename(path))[0][:31]

            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Archivo Excel generado: {OUTPUT_FILE}")
    print("Pestañas creadas:")
    for path in JSON_FILES:
        print(" -", os.path.splitext(os.path.basename(path))[0])

if __name__ == "__main__":
    main()
