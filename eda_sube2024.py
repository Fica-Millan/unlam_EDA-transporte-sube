import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# 1️⃣ ----- C A R G A   D E L   D A T A S E T -----
df = pd.read_csv("df-sube-2024.csv", parse_dates=["DIA_TRANSPORTE"])

# 2️⃣ ----- P R I M E R   V I S T A Z O -----
print("─" * 80 + "\nDIMENSIONES DEL DATASET SUBE 2024\n")
print(df.shape)

print("─" * 80 + "\nINFORMACION GENERAL DEL DATASET\n")
df.info()

print("─" * 80 + "\nRANGO DE FECHAS DE 'DIA_TRANSPORTE'\n")
print("Rango de fechas:", df["DIA_TRANSPORTE"].min(), "a", df["DIA_TRANSPORTE"].max())

print("─" * 80 + "\nESTADÍSTICAS DESCRIPTIVAS (NUMÉRICAS)\n")
print(df.describe(include=[np.number]).round(2)) # filtra que solo se incluyan columnas de tipo numérico y con 2 decimales

# Verificación de duplicados
print("─" * 80 + "\nVERIFICACIÓN DE DUPLICADOS\n")
print("Duplicados:", df.duplicated().sum())


# 3️⃣ ----- E S T A D Í S T I C A S   D E S C R I P T I V A S -----
# 🔸 Detectar filas con valores negativos en la columna 'CANTIDAD'
negativos = df[df["CANTIDAD"] < 0]
print("\nCantidad de filas con valores negativos en CANTIDAD:", len(negativos))
print(negativos[["DIA_TRANSPORTE", "TIPO_TRANSPORTE", "CANTIDAD"]].head(10))
print("\n⚠️  Se encontraron 3 valores anómalos en CANTIDAD (valores negativos). Estos se consideran errores o correcciones no documentadas.")

# 🔸 Eliminar filas con valores negativos en 'CANTIDAD' para evitar problemas en el análisis
df = df[df["CANTIDAD"] >= 0]
print("✔️  Filas con valores negativos en 'CANTIDAD' eliminadas correctamente.")

# 🔸 Mostrar resumen estadístico actualizado de la columna 'CANTIDAD'
print("─" * 50 + "\nESTADÍSTICAS ACTUALIZADAS\n" + "─" * 50)
print("Resumen estadístico de la columna CANTIDAD:")
print(df["CANTIDAD"].describe().round(2))


# 🔸 Histograma de la variable 'CANTIDAD' (antes de la transformación)
plt.figure()
df["CANTIDAD"].hist(bins=50, color="salmon", grid=False)
plt.title("Distribución de CANTIDAD de viajes")
plt.xlabel("Cantidad de viajes")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("graficos/sube2024_histograma_cantidad.png")


# 🔸Aplicar transformación logarítmica para reducir la asimetría de la distribución
df["CANTIDAD_LOG"] = np.log1p(df["CANTIDAD"]) # Se usa log1p para evitar problemas con ceros (log(0) no está definido)


# 🔸 Histograma de la variable transformada 'CANTIDAD_LOG'
plt.figure()
df["CANTIDAD_LOG"].hist(bins=50, color="lightseagreen", grid=False)
plt.title("Distribución logarítmica de CANTIDAD")
plt.xlabel("log(1 + Cantidad de viajes)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("graficos/sube2024_histograma_cantidad_log.png")


# 4️⃣ ----- R E V I S A R   C O L U M N A S   C O N S T A N T E S (desvío estándar = 0) -----
print("─" * 50 + "\nCOLUMNAS CON DESVIACION ESTANDAR = 0\n")
stds = df.std(numeric_only=True)    # Calcula la desviación estándar solo de las columnas numéricas
cero_std = stds[stds == 0.0]        # Filtra las columnas cuya desviación estándar es exactamente cero (es decir, columnas constantes)
print(cero_std if not cero_std.empty else "Ninguna columna numérica es constante.")


# 5️⃣ ----- V A L O R E S   F A L T A N T E S  -----
print("─" * 50 + "\nVALORES FALTANTES POR COLUMNA\n" + "─" * 50)
print(df.isna().sum()) # Devuelve un df del mismo tamaño con valores booleanos, luego suma los True por columna

print("\n----- ANÁLISIS DE VALORES NULOS -----")

# Filas con JURISDICCION nula
nulos_jur = df[df["JURISDICCION"].isna()]
print("\nTipos de transporte con JURISDICCION nula:")
print(nulos_jur["TIPO_TRANSPORTE"].value_counts())

# Filas con PROVINCIA nula
nulos_prov = df[df["PROVINCIA"].isna()]
print("\nTipos de transporte con PROVINCIA nula:")
print(nulos_prov["TIPO_TRANSPORTE"].value_counts())

# Filas con MUNICIPIO nulo
nulos_mun = df[df["MUNICIPIO"].isna()]
print("\nTipos de transporte con MUNICIPIO nulo:")
print(nulos_mun["TIPO_TRANSPORTE"].value_counts())

# Correccion datos nulos
es_subte = df["TIPO_TRANSPORTE"] == "SUBTE" # Filtrar filas donde TIPO_TRANSPORTE es SUBTE
df.loc[es_subte, "JURISDICCION"] = df.loc[es_subte, "JURISDICCION"].fillna("CABA")  # Completar valores nulos con información conocida
df.loc[es_subte, "PROVINCIA"] = df.loc[es_subte, "PROVINCIA"].fillna("CIUDAD AUTÓNOMA DE BUENOS AIRES")
df.loc[es_subte, "MUNICIPIO"] = df.loc[es_subte, "MUNICIPIO"].fillna("CABA")

# Verificación final de nulos
print("\n----- Verificación de valores nulos tras corrección en SUBTE -----")
print(df[["JURISDICCION", "PROVINCIA", "MUNICIPIO"]].isna().sum())

# Filas con PROVINCIA nula
nulos_prov = df[df["PROVINCIA"].isna()]
print("\nValores Nulos por Provincia:")
print(nulos_prov[["TIPO_TRANSPORTE", "NOMBRE_EMPRESA", "LINEA", "AMBA"]].to_string(index=False))

# Filas con MUNICIPIO nulo
nulos_mun = df[df["MUNICIPIO"].isna()]
print("\nValores Nulos por Municipio:")
print(nulos_mun[["TIPO_TRANSPORTE", "NOMBRE_EMPRESA", "LINEA", "AMBA"]].to_string(index=False))

# COLECTIVO – Empresa 9 de Julio SRL – Línea 500 Santa Fe
colectivo_sfe = (df["TIPO_TRANSPORTE"] == "COLECTIVO") & (df["LINEA"] == "LINEA_500I_SFE")
df.loc[colectivo_sfe, "PROVINCIA"] = "SANTA FE"
df.loc[colectivo_sfe, "MUNICIPIO"] = "SANTA FE"

# TREN – Tren del Valle
tren_valle = (df["TIPO_TRANSPORTE"] == "TREN") & (df["LINEA"] == "FFCC TREN DEL VALLE")
df.loc[tren_valle, "PROVINCIA"] = "JN"
df.loc[tren_valle, "MUNICIPIO"] = "SD"

print("\n----- Verificación final tras imputación específica: -----")
print(df[["JURISDICCION", "PROVINCIA", "MUNICIPIO"]].isna().sum())
print("\n✔️  Filas con valores nulos corregidas correctamente.")


# 6️⃣ ----- O U T L I E R S -----
# Estadísticas descriptivas por AMBA (si/no)
print("\n----- Estadísticas descriptivas -----")
print(df.groupby('AMBA')['CANTIDAD'].describe())

# Boxplot para comparar distribuciones por AMBA
plt.figure(figsize=(10,6))
sns.boxplot(x='AMBA', y='CANTIDAD', data=df)
plt.title('Distribución de CANTIDAD según AMBA')
plt.xlabel('AMBA (si/no)')
plt.ylabel('CANTIDAD')
plt.tight_layout()
plt.savefig("graficos/sube2024_boxplot_amba.png")

print("\n----- Identificación de outliers por AMBA (sin eliminar) -----")
def identificar_outliers_por_grupo(df, columna_grupo, columna_valor):
    for grupo, subdf in df.groupby(columna_grupo):
        Q1 = subdf[columna_valor].quantile(0.25)
        Q3 = subdf[columna_valor].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = max(Q1 - 1.5 * IQR, 0)
        upper_bound = Q3 + 1.5 * IQR
        
        total = len(subdf)
        normales = subdf[(subdf[columna_valor] >= lower_bound) & (subdf[columna_valor] <= upper_bound)]
        outliers = total - len(normales)
        
        print(f"{columna_grupo} = {grupo}")
        print(f"  Q1: {Q1:.1f}, Q3: {Q3:.1f}, IQR: {IQR:.1f}")
        print(f"  Rango normal: [{lower_bound:.1f}, {upper_bound:.1f}]")
        print(f"  Total filas: {total}, Outliers detectados: {outliers}\n")
        
# Llamamos a la función pero NO reasignamos df
identificar_outliers_por_grupo(df, 'AMBA', 'CANTIDAD')

print("----- Análisis de outliers -----")
print("⚠️  Los valores considerados outliers podrían corresponder a situaciones reales")
print("(eventos masivos, paros, problemas técnicos), por lo que se optó por mantenerlos.")
print("En lugar de eliminarlos, se los identificó y analizó por separado para entender su impacto.\n")


# 7️⃣ ----- P E R F I L   T E M P O R A L -----
df["MES"] = df["DIA_TRANSPORTE"].dt.month # Extrae el nº de mes de la columna "DIA_TRANSPORTE" y crea la columna "MES" con ese valor


# 🔸Total de viajes por mes
viajes_mes = df.groupby("MES")["CANTIDAD"].sum() # Agrupa el df por columna "MES", suma los valores de columna "CANTIDAD" y guarda resultado en viajes_mes
plt.figure()                                     
viajes_mes.plot(kind="bar", color="cyan")        # viajes_mes es una serie con meses como índice y la suma de viajes como valores - gráfico de barras
plt.title("Total de viajes por mes (2024)")
plt.xlabel("Mes")
plt.ylabel("Cantidad de viajes")
  
# Agregar etiquetas a las barras con rotación y separación vertical
for i, v in enumerate(viajes_mes):
    plt.text(i, v - 80_000_000, f"{int(v):,}", ha='center', va='bottom', fontsize=8, rotation=90)
    
plt.tight_layout()
plt.savefig("graficos/sube2024_viajes_por_mes.png")


# 🔸Total de viajes por día de la semana
orden_dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
viajes_dsem = df.groupby("DIA_SEMANA")["CANTIDAD"].sum().reindex(orden_dias) # reindex cambia el orden del índice de la serie pq coincida con el orden establecido
plt.figure()
viajes_dsem.plot(kind="bar", color="coral")
plt.title("Total de viajes por día de la semana")
plt.xlabel("Día de la semana")
plt.ylabel("Cantidad de viajes")

# Agregar etiquetas a las barras con rotación y separación vertical
for i, v in enumerate(viajes_dsem):
    plt.text(i, v - 180_000_000, f"{int(v):,}", ha='center', va='bottom', fontsize=8, rotation=90)
    
plt.tight_layout()
plt.savefig("graficos/sube2024_viajes_por_dia_semana.png")


# 🔸Evolucion mensual por tipo de transporte
df['MES_ANO'] = df['DIA_TRANSPORTE'].dt.to_period('M').astype(str) # Crear columna MES_ANO

# Agrupar por MES_ANO y TIPO_TRANSPORTE
df_mes = (
    df
    .groupby(['MES_ANO', 'TIPO_TRANSPORTE'])['CANTIDAD']
    .sum()
    .reset_index()
)

# Asegurar orden cronológico de los meses
df_mes['MES_ANO'] = pd.to_datetime(df_mes['MES_ANO'])
df_mes = df_mes.sort_values('MES_ANO')

plt.figure(figsize=(12,6))
sns.lineplot(
    data=df_mes,
    x='MES_ANO',
    y='CANTIDAD',
    hue='TIPO_TRANSPORTE',
    marker='o'
)

plt.title('Evolución mensual de viajes por tipo de transporte - 2024')
plt.xlabel('Mes')
plt.ylabel('Cantidad de viajes')
plt.xticks(rotation=45)
plt.legend(title='Tipo de transporte', bbox_to_anchor=(1.02,1), loc='upper left')
plt.tight_layout()
plt.savefig("graficos/sube2024_evolucion_mensual.png")


# 8️⃣ ----- P E R F I L   P O R   C A T E G O R I A -----
# 🔸Por tipo de transporte
viajes_tipo = df.groupby("TIPO_TRANSPORTE")["CANTIDAD"].sum()
plt.figure()
colores = ["#B0E0E6", "#87CEEB", "#C1E1C1", "#A7C7E7", "#C6E2FF", "#98FB98"]  
viajes_tipo.plot(           # Graficar pie chart con etiquetas separadas y sin decimales en porcentajes
    kind="pie",
    autopct='%1.1f%%',      # un decimal
    startangle=90,
    pctdistance=0.85,       # distancia del porcentaje al centro
    labeldistance=1.12,     # distancia de las etiquetas fuera de la torta
    colors=colores
)
plt.title("Distribución de viajes por tipo de transporte")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graficos/sube2024_viajes_por_tipo_transporte.png")


# 🔸Comparativa: HÁBIL / FERIADO / FIN DE SEMANA
# Agrupamos por día (fecha) y sumamos los viajes totales de ese día
viajes_diarios = df.groupby(["DIA_TRANSPORTE", "TIPO_DIA"])["CANTIDAD"].sum().reset_index()

# Se calcula el promedio diario por tipo de día
promedios = viajes_diarios.groupby("TIPO_DIA")["CANTIDAD"].mean()

plt.figure()
ax = promedios.plot(kind="bar", color="#C1E1C1")

plt.title("Viajes promedio por tipo de día")
plt.xlabel("Tipo de día")
plt.ylabel("Promedio de viajes")
plt.tight_layout()

# Agregar valores dentro de las barras
for i, valor in enumerate(promedios):
    ax.text(i, valor * 0.95, f'{valor:,.0f}', ha='center', va='top', color='black')

plt.savefig("graficos/sube2024_promedio_viajes_tipo_dia.png")


# 🔸Días hábil vs no hábil
df["ES_HABIL"] = df["TIPO_DIA"] == "HÁBIL"
conteo_habiles = df.groupby("ES_HABIL")["CANTIDAD"].sum()

# Calcular porcentajes
total = conteo_habiles.sum()
porcentajes = (conteo_habiles / total * 100).round(1)

plt.figure()
bars = conteo_habiles.plot(kind="bar", color=["#FF6347", "#3CB371"])
plt.title("Total de viajes: días hábiles vs no hábiles")
plt.xlabel("¿Es día hábil?")
plt.ylabel("Cantidad de viajes")
plt.xticks([0, 1], labels=["No", "Sí"], rotation=0)

# Agregar etiquetas de porcentaje sobre cada barra
for i, (valor, porcentaje) in enumerate(zip(conteo_habiles, porcentajes)):
    plt.text(i, valor, f"{porcentaje}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("graficos/sube2024_viajes_habil_vs_no.png")


# 9️⃣ ----- B O X P L O T   D E   C A N T I D A D   P O R   T I P O   D E   T R A N S P O R T E -----
plt.figure()
df.boxplot(column="CANTIDAD", by="TIPO_TRANSPORTE", grid=False) # dibuja el boxplot agrupado por tipo de transporte, sin mostrar la cuadrícula.
plt.yscale("log")  # Mejora la visualización si hay outliers extremos
plt.title("Distribución de viajes por tipo de transporte")
plt.suptitle("")
plt.xlabel("Tipo de transporte")
plt.ylabel("Cantidad de viajes")
plt.tight_layout()
plt.savefig("graficos/sube2024_boxplot_cantidad_por_tipo.png")


# 1️⃣0️⃣----- A N A L I S I S   D E   C A N T I D A D   D E   V I A J E S   P O R   M O T I V O   D E   F E R I A D O -----
# Filtrar solo los días feriados reales con motivo válido
feriados_df = df[(df["TIPO_DIA"] == "FERIADO") & (df["MOTIVO_FERIADO"] != "NO FERIADO")].copy()

# Agrupar por motivo del feriado y sumar cantidad de viajes
viajes_por_feriado = feriados_df.groupby("MOTIVO_FERIADO")["CANTIDAD"].sum().sort_values(ascending=True)

plt.figure(figsize=(10, 6))
viajes_por_feriado.plot(kind="barh", color="#DFBFF3")

# Agregar valores al final de cada barra
for i, (valor, label) in enumerate(zip(viajes_por_feriado, viajes_por_feriado.index)):
    plt.text(valor - 1000, i, f"{int(valor):,}", va="center", ha="right", color="black", fontsize=9)
    
plt.xlabel("Cantidad total de viajes")
plt.ylabel("Motivo del feriado")
plt.title("Cantidad de viajes por feriado (2024)")
plt.tight_layout()
plt.savefig("graficos/sube2024_cantidad_viajes_por_feriado.png")


# 1️⃣1️⃣----- C A N T I D A D   T O T A L   D E   V I A J E S   P O R   D I A   D E   L A   S E M A N A   Y   T I P O   D E   T R A N S P O R T E ----- 
# Agrupar por día de la semana y tipo de transporte sumando la cantidad de viajes
tabla_pivot = df.pivot_table(
    index="DIA_SEMANA", 
    columns="TIPO_TRANSPORTE", 
    values="CANTIDAD", 
    aggfunc="sum"
)

# Reordenar filas para que el orden de los días sea correcto
orden_dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
tabla_pivot = tabla_pivot.reindex(orden_dias)

# Graficar heatmap con seaborn
plt.figure(figsize=(10,6))
sns.heatmap(
    tabla_pivot, 
    annot=True,        # Mostrar los valores dentro de cada celda
    fmt=".0f",         # Sin decimales
    cmap="Reds",       # Paleta de colores
    cbar_kws={'label': 'Cantidad de viajes'}
)

plt.title("Cantidad total de viajes por día de la semana y tipo de transporte (2024)")
plt.xlabel("Tipo de transporte")
plt.ylabel("Día de la semana")
plt.tight_layout()
plt.savefig("graficos/sube2024_heatmap_dia_semana_tipo_transporte.png")


#1️⃣2️⃣----- M E N S A J E S   F I N A L E S   D E   C O N F I R M A C I O N -----
print("\n✅ El análisis EDA se completo correctamente.")
print("✅ El análisis fue realizado sin excluir registros del dataset principal.\n")
print("📊 Se generaron los siguientes archivos:")
print(" - sube2024_boxplot_amba.png")
print(" - sube2024_boxplot_cantidad_por_tipo.png")
print(" - sube2024_cantidad_viajes_por_feriado.png")
print(" - sube2024_evolucion_mensual.png")
print(" - sube2024_heatmap_dia_semana_tipo_transporte.png")
print(" - sube2024_histograma_cantidad.png")
print(" - sube2024_histograma_cantidad_log.png")
print(" - sube2024_promedio_viajes_tipo_dia.png")
print(" - sube2024_viajes_habil_vs_no_habil.png")
print(" - sube2024_viajes_por_dia_semana.png")
print(" - sube2024_viajes_por_mes.png")
print(" - sube2024_viajes_por_tipo_transporte.png")

# 5. Guardar resultado
df.to_csv("dat_sube2024_eda.csv", index=False, encoding="utf-8-sig")
print("✅ Datos limpios y procesados son guardados en 'dat_sube2024_eda.csv'")

print("\nProceso terminado.\n\n")  