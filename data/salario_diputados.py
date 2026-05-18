"""
Scraping de salarios de diputados — Transparentia (Newtral)
===========================================================
Lee Libro1.xlsx, construye la URL de cada ficha y extrae los 5 campos
de salario directamente del HTML estático (no necesita Selenium).

Requisitos:
    pip install requests beautifulsoup4 pandas openpyxl unidecode

Uso:
    python scraping_v2.py
"""

import re
import time
import unicodedata
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ── Configuración ────────────────────────────────────────────────────────────

EXCEL_ENTRADA  = "Libro1.xlsx"
EXCEL_SALIDA   = "diputados_transparentia.xlsx"
CSV_SALIDA     = "diputados_transparentia.csv"
BASE_URL       = "https://transparentia.newtral.es/ficha/"
PAUSA          = 1.2   # segundos entre peticiones
MAX_REINTENTOS = 3

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}

# Mapeo etiqueta HTML → columna del Excel
CAMPOS = {
    "Salario bruto mensual:": "SALARIO_BRUTO_MENSUAL",
    "Salario bruto anual:":   "SALARIO_BRUTO_ANUAL",
    "Salario base:":          "SALARIO_BASE",
    "Suplementos:":           "SUPLEMENTOS",
    "Dietas:":                "DIETAS",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def nombre_a_slug(nombre: str, apellidos: str) -> str:
    texto = unicodedata.normalize("NFD", f"{nombre} {apellidos}")
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def limpiar_importe(valor: str) -> float:
    """Convierte '5.651,41 €' → 5651.41"""
    limpio = re.sub(r"[€\s]", "", valor).replace(".", "").replace(",", ".")
    try:
        return float(limpio)
    except ValueError:
        return float("nan")


def extraer_salarios(url: str, session: requests.Session) -> dict:
    """
    Descarga la ficha y extrae los 5 campos de salario de la tabla
    'Especificaciones sobre el salario'.
    Devuelve un dict con las columnas del Excel como claves.
    """
    resultado = {col: float("nan") for col in CAMPOS.values()}
    resultado["URL"] = url
    resultado["ESTADO"] = "OK"

    for intento in range(MAX_REINTENTOS):
        try:
            r = session.get(url, headers=HEADERS, timeout=15)
            break
        except requests.RequestException as e:
            if intento == MAX_REINTENTOS - 1:
                resultado["ESTADO"] = f"Error conexión: {e}"
                return resultado
            time.sleep(2)

    if r.status_code == 404:
        resultado["ESTADO"] = "404 - No encontrado"
        return resultado
    if r.status_code != 200:
        resultado["ESTADO"] = f"HTTP {r.status_code}"
        return resultado

    soup = BeautifulSoup(r.text, "html.parser")

    # Localizar la tabla por su cabecera
    tabla = None
    for th in soup.find_all("th"):
        if "Especificaciones" in (th.text or ""):
            tabla = th.find_parent("table")
            break

    if not tabla:
        resultado["ESTADO"] = "Tabla no encontrada"
        return resultado

    # Recorrer todas las filas de tbody + tfoot
    for fila in tabla.find_all("tr"):
        celdas = fila.find_all(["th", "td"])
        if len(celdas) < 2:
            continue
        etiqueta = celdas[0].text.strip()
        valor    = celdas[1].text.strip()
        if etiqueta in CAMPOS:
            resultado[CAMPOS[etiqueta]] = limpiar_importe(valor)

    return resultado


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Transparentia Scraper v2 — Salarios de diputados")
    print("=" * 60)

    df = pd.read_excel(EXCEL_ENTRADA)
    total = len(df)
    print(f"\nDiputados: {total}")

    # Columnas de salario que vamos a rellenar (sobrescribir con datos frescos)
    cols_salario = list(CAMPOS.values())
    for col in cols_salario:
        if col not in df.columns:
            df[col] = float("nan")

    session = requests.Session()
    errores = []

    for i, row in df.iterrows():
        slug = nombre_a_slug(str(row["NOMBRE"]), str(row["APELLIDOS"]))
        url  = BASE_URL + slug
        print(f"[{i+1:>3}/{total}] {row['NOMBRE']} {row['APELLIDOS']}", end=" ... ")

        datos = extraer_salarios(url, session)
        estado = datos.pop("ESTADO")
        datos.pop("URL", None)

        if estado == "OK":
            for col, val in datos.items():
                df.at[i, col] = val
            vals = [f"{col.split('_')[-1]}: {val:,.2f}€" for col, val in datos.items() if val == val]
            print(f"✓  {' | '.join(vals)}")
        else:
            print(f"✗  {estado}")
            errores.append({"fila": i+1, "diputado": f"{row['NOMBRE']} {row['APELLIDOS']}", "error": estado, "url": url})

        time.sleep(PAUSA)

    # Exportar
    df.to_csv(CSV_SALIDA, index=False, encoding="utf-8-sig")
    df.to_excel(EXCEL_SALIDA, index=False)
    print(f"\n✓ CSV   → {CSV_SALIDA}")
    print(f"✓ Excel → {EXCEL_SALIDA}")

    if errores:
        df_err = pd.DataFrame(errores)
        df_err.to_csv("errores_scraping.csv", index=False, encoding="utf-8-sig")
        print(f"⚠ {len(errores)} errores → errores_scraping.csv")

    print(f"\nResumen:")
    for col in cols_salario:
        n = df[col].notna().sum()
        print(f"  {col}: {n}/{total} diputados con dato")


if __name__ == "__main__":
    main()