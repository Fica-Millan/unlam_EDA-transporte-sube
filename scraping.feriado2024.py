import requests                 # Para realizar peticiones HTTP
from bs4 import BeautifulSoup   # Para parsear el contenido HTML    
import pandas as pd             # Para manipulación de datos con DataFrames
from datetime import datetime   # Para manejar fechas
import re                       # Para trabajar con expresiones regulares

# Mapeo de nombres de meses en español a su número correspondiente
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

# Diccionario vacío para almacenar los feriados encontrados
feriados = {}

# 1. Descargar y parsear la página de feriados de La Nación para el año 2024
url = "https://www.lanacion.com.ar/feriados/2024/"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(resp.content, "html.parser")

# 2. Buscar todos los bloques de calendario mensual en la página
calendarios = soup.find_all("div", class_="holidays-card-calendar")

# 2.1 Iterar sobre cada mes encontrado
for calendario in calendarios:
    # Extraer el encabezado del calendario mensual
    encabezado = calendario.find("div", class_="labeled-calendar")
    if not encabezado:
        continue    # Saltar si no se encuentra el encabezado

    # Buscar el nombre del mes dentro del enlace    
    link_mes = encabezado.find("a", class_="com-link")
    if not link_mes:
        continue    # Saltar si no se encuentra el enlace

    # Obtener el nombre y número del mes
    nombre_mes = link_mes.text.strip().lower()
    numero_mes = meses.get(nombre_mes)
    if not numero_mes:
        print(f"⚠️ Mes no reconocido: {nombre_mes}")
        continue

    # Buscar la lista de feriados del mes    
    ul = calendario.find("ul", class_="holidays-list")
    if not ul:
        continue    # Saltar si no se encuentra la lista

    # Iterar sobre cada feriado del mes
    for li in ul.find_all("li"):
        # Buscar el día del feriado y el motivo
        dia_tag = li.find("span", class_=re.compile(r"--"))     # Tag con el día
        motivo_tag = li.find("h4", class_="com-text")           # Tag con el motivo
        if not dia_tag or not motivo_tag:
            continue        # Saltar si falta alguno de los datos

        try:
            # Parsear día y motivo, y construir la fecha completa en formato YYYY-MM-DD
            dia = int(dia_tag.text.strip())
            motivo = motivo_tag.text.strip().upper()
            fecha = datetime(2024, numero_mes, dia).strftime("%Y-%m-%d")
            
            # Guardar la fecha y el motivo en el diccionario
            feriados[fecha] = motivo
        except Exception as e:
            # Mostrar error si ocurre al intentar procesar una entrada
            print(f"❌ Error procesando {nombre_mes} {li}: {e}")

# 3. Mostrar los feriados encontrados en consola
print("Feriados encontrados:")
for fecha, motivo in sorted(feriados.items()):
    print(f"{fecha} → {motivo}")

# 4. Leer archivo CSV con datos de SUBE y etiquetar si el día es feriado
df_sube = pd.read_csv("df-sube-2024-tipo-dia.csv", parse_dates=["DIA_TRANSPORTE"])

# Crear nueva columna con el motivo del feriado (o "NO FERIADO" si no aplica)
df_sube["MOTIVO_FERIADO"] = df_sube["DIA_TRANSPORTE"].dt.strftime("%Y-%m-%d").map(feriados).fillna("NO FERIADO")

# 5. Guardar el DataFrame resultante en un nuevo archivo CSV
df_sube.to_csv("df-sube-2024.csv", index=False, encoding="utf-8-sig")

# Mensajes de confirmación final
print("✅ Scraping finalizado. Archivo guardado como df-sube-2024.csv")
print(f"✅ Total de feriados encontrados: {len(feriados)}")
