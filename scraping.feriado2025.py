import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

# Mapeo de nombres de meses en español a número de mes
meses = {
    "enero":   1,
    "febrero": 2,
    "marzo":   3,
    "abril":   4,
    "mayo":    5,
    "junio":   6,
    "julio":   7,
    "agosto":  8,
    "septiembre": 9,
    "octubre":   10,
    "noviembre": 11,
    "diciembre": 12
}

feriados = {}

# 1. Descargar y parsear la página de feriados 2025
url = "https://www.lanacion.com.ar/feriados/2025/"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(resp.content, "html.parser")

# 2. Buscar cada bloque mensual
calendarios = soup.find_all("div", class_="holidays-card-calendar")

for calendario in calendarios:
    # 2.1 Extraer el nombre del mes desde el <a class="com-link">
    encabezado = calendario.find("div", class_="labeled-calendar")
    if not encabezado:
        continue

    link_mes = encabezado.find("a", class_="com-link")
    if not link_mes:
        continue

    nombre_mes = link_mes.text.strip().lower()
    numero_mes = meses.get(nombre_mes)
    if not numero_mes:
        print(f"⚠️ Mes no reconocido: {nombre_mes}")
        continue

    # 2.2 Iterar la lista de feriados de ese mes
    ul = calendario.find("ul", class_="holidays-list")
    if not ul:
        continue

    for li in ul.find_all("li"):
        dia_tag = li.find("span", class_=re.compile(r"--"))
        motivo_tag = li.find("h4", class_="com-text")
        if not dia_tag or not motivo_tag:
            continue

        try:
            dia = int(dia_tag.text.strip())
            motivo = motivo_tag.text.strip().upper()
            fecha = datetime(2025, numero_mes, dia).strftime("%Y-%m-%d")
            feriados[fecha] = motivo
        except Exception as e:
            print(f"❌ Error procesando {nombre_mes} {li}: {e}")

# 3. Mostrar resultados en consola
print("Feriados encontrados:")
for fecha, motivo in sorted(feriados.items()):
    print(f"{fecha} → {motivo}")

# 4. Leer CSV de SUBE y etiquetar feriados
df_sube = pd.read_csv("df-sube-2025-tipo-dia.csv", parse_dates=["DIA_TRANSPORTE"])
df_sube["MOTIVO_FERIADO"] = df_sube["DIA_TRANSPORTE"].dt.strftime("%Y-%m-%d").map(feriados).fillna("NO FERIADO")

# 5. Guardar resultado
df_sube.to_csv("df-sube-2025.csv", index=False, encoding="utf-8-sig")
print("✅ Scraping finalizado. Archivo guardado como df-sube-2025.csv")
print(f"✅ Total de feriados encontrados: {len(feriados)}")
