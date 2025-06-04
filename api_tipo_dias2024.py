import requests          # Para realizar peticiones HTTP a una API
import pandas as pd      # Para manipulación y análisis de datos en DataFrames

# 1) Leer el dataset y convierte la columna DIA_TRANSPORTE a formato de fecha 
df_sube = pd.read_csv("dat-ab-usos-2024.csv", parse_dates=["DIA_TRANSPORTE"])

# 2) Obtener la lista de feriados en Argentina para 2024 desde la API pública de Nager.Date
feriados_2024 = requests.get("https://date.nager.at/api/v3/PublicHolidays/2024/AR").json()

# Extraer solo las fechas en formato string y guardarlas en un set para evitar duplicados
fechas_feriados = set(item["date"] for item in feriados_2024) 

# 3) Función para clasificar cada fecha como FERIADO, FIN_DE_SEMANA o HÁBIL
def clasificar_fecha(fecha): 
    fecha_str = fecha.strftime("%Y-%m-%d")  # Convertir la fecha a string con formato YYYY-MM-DD
    if fecha_str in fechas_feriados:
        return "FERIADO"
    elif fecha.weekday() >= 5:              # devuelve un número Sábado (5) o domingo (6)
        return "FIN_DE_SEMANA"
    else:
        return "HÁBIL"

# 4) Diccionario para traducir el nombre del día de la semana al español
dias_traduccion = {
    "Monday": "LUNES", "Tuesday": "MARTES", "Wednesday": "MIÉRCOLES",
    "Thursday": "JUEVES", "Friday": "VIERNES", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
}
# Agregar una nueva columna con el nombre del día de la semana en español
df_sube["DIA_SEMANA"] = df_sube["DIA_TRANSPORTE"].dt.day_name().map(dias_traduccion)

# 5) Aplicar la función de clasificación a cada fila del DataFrame
df_sube["TIPO_DIA"] = df_sube["DIA_TRANSPORTE"].apply(clasificar_fecha)

# 6) Guardar el nuevo dataset con las columnas agregadas
df_sube.to_csv("df-sube-2024-tipo-dia.csv", index=False, encoding="utf-8-sig")
# index=False           → No guarda el índice del DataFrame como columna en el CSV
# encoding="utf-8-sig"  → Asegura que Excel reconozca correctamente los caracteres especiales

# Mensaje de confirmación
print('✅ Proceso finalizado. Se han agregado las columnas "DIA_SEMANA" y "TIPO_DIA" (desde API) al Dataset.')
print('📁 Archivo guardado como: df-sube-2024-tipo-dia.csv')