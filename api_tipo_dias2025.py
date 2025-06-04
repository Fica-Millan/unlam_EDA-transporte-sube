import requests          # librería para hacer peticiones HTTP
import pandas as pd      # librería estándar para trabajar con dataframes

# 1) Leer el dataset y convierte la columna DIA_TRANSPORTE a formato de fecha 
df_sube = pd.read_csv("https://archivos-datos.transporte.gob.ar/upload/Dat_Ab_Usos/dat-ab-usos-2025.csv", parse_dates=["DIA_TRANSPORTE"])

# 2) Obtener feriados de Argentina en 2025
feriados_2025 = requests.get("https://date.nager.at/api/v3/PublicHolidays/2025/AR").json()
fechas_feriados = set(item["date"] for item in feriados_2025) # El uso de set(...) garantiza que las fechas estén sin duplicados

# 3) Función para clasificar cada fecha
def clasificar_fecha(fecha): # se define la funcion clasificar_fecha del parametro fecha
    fecha_str = fecha.strftime("%Y-%m-%d")
    if fecha_str in fechas_feriados:
        return "FERIADO"
    elif fecha.weekday() >= 5:  # .weekday() devuelve un número de 0 a 6 (5=sábado, 6=domingo)
        return "FIN_DE_SEMANA"
    else:
        return "HÁBIL"

# 4) Día de la semana traducido
dias_traduccion = {
    "Monday": "LUNES", "Tuesday": "MARTES", "Wednesday": "MIÉRCOLES",
    "Thursday": "JUEVES", "Friday": "VIERNES", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
}
df_sube["DIA_SEMANA"] = df_sube["DIA_TRANSPORTE"].dt.day_name().map(dias_traduccion)

# 5) Clasificación del tipo de día
df_sube["TIPO_DIA"] = df_sube["DIA_TRANSPORTE"].apply(clasificar_fecha)

# 6) Guardar el nuevo dataset
df_sube.to_csv("df-sube-2025-tipo-dia.csv", index=False, encoding="utf-8-sig")
# index=False → Le dice a pandas que no incluya la columna del índice
# encoding="utf-8-sig" → Especifica el tipo de codificación útil si después usas Excel
print('✅ Proceso finalizado. Se han agregado las columnas "DIA_SEMANA" y "TIPO_DIA" (desde API) al Dataset.')
print('📁 Archivo guardado como: df-sube-2025-tipo-dia.csv')
