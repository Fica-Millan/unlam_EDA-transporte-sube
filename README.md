
# Análisis de la Demanda de Transporte Público mediante Datos SUBE (2024/2025)

Trabajo Práctico final de la materia **Captura y Almacenamiento de Datos** - Especialización en Ciencia de Datos - UNLaM  
Grupo 4 - Año 2025  

## 📝 Descripción

Este trabajo analiza la demanda del transporte público en Argentina utilizando datos públicos del sistema SUBE, correspondientes al año 2024 y los primeros cinco meses del 2025.  
Se aplicaron técnicas de **limpieza de datos**, **enriquecimiento mediante APIs y scraping**, y **análisis exploratorio (EDA)** tanto univariado como bivariado.

---

## ▶️ Orden de ejecución sugerido

1. `api_tipo_dias2024.py`  
2. `api_tipo_dias2025.py`  
3. `scraping_consulta_robots.py` *(opcional, para verificar permisos)*  
4. `scraping_feriados2024.py`  
5. `scraping_feriados2025.py`  
6. `eda_sube2024.py`  
7. `eda_sube2025.py`  
8. `comparativa_2025vs2024.py`


## 📂 Estructura del proyecto

```bash
.
├── docs/
│   ├── informe_final.pdf
│   └── presentacion.pdf
├── graficos/
│   ├── eda_2024_*.png
│   ├── eda_2025_*.png
│   └── comparativa_*.png
└── README.md
├── api_tipo_dias2024.py
├── api_tipo_dias2025.py
├── comparativa_2025vs2024.py
├── df-sube-2024.csv
├── df-sube-2025.csv
├── eda_sube2024.py
├── eda_sube2025.py
├── scraping_feriados2024.py
├── scraping_feriados2025.py
├── scraping_consulta_robots.py

```

## 📜 Detalle de los scripts

El proyecto se compone de los siguientes scripts:

### 1. Clasificación de días (`api_tipo_dias2024.py` y `api_tipo_dias2025.py`)
Enriquece el dataset original incorporando dos nuevas columnas:
- `DIA_SEMANA`: nombre del día en español.
- `TIPO_DIA`: clasificado como HÁBIL, FERIADO o FIN_DE_SEMANA, utilizando la API pública de feriados de Nager.Date.

Salida:  
- `df-sube-2024-tipo-dia.csv`  
- `df-sube-2025-tipo-dia.csv`

---

### 2. Verificación de permisos de scraping (`scraping_consulta_robots.py`)
Consulta el archivo `robots.txt` del sitio de La Nación para verificar que se permite el scraping de las páginas de feriados.

---

### 3. Scraping de feriados (`scraping_feriados2024.py` y `scraping_feriados2025.py`)
Obtiene el listado y motivo de los feriados nacionales desde el sitio web de La Nación y agrega una nueva columna:
- `MOTIVO_FERIADO`

Entrada:  
- `df-sube-2024-tipo-dia.csv`  
- `df-sube-2025-tipo-dia.csv`  

Salida:  
- `df-sube-2024.csv`  
- `df-sube-2025.csv`

---

### 4. Análisis exploratorio (`eda_sube2024.py` y `eda_sube2025.py`)
Realiza limpieza de datos (detección de outliers, valores nulos, estandarización), generación de variables derivadas y análisis univariado y bivariado del dataset.

Entrada esperada:  
- `df-sube-2024.csv`  
- `df-sube-2025.csv`

---

### 5. Comparación interanual (`comparativa_2025vs2024.py`)
Compara la evolución de la demanda de transporte entre enero–mayo de 2024 y 2025 por tipo de transporte y tipo de día.

---

## 📦 Requisitos

- Python 3.8 o superior
- Bibliotecas:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `requests`
  - `beautifulsoup4`

Instalación con `pip`:

```bash
pip install pandas numpy matplotlib seaborn requests beautifulsoup4
```

---

## 📁 Fuentes de datos

- [Dataset oficial SUBE 2024](https://datos.transporte.gob.ar/dataset/sube-cantidad-de-transacciones-usos-por-fecha/archivo/c7dad6d8-8fe4-449e-82c9-18ed8574eae8)
- [Dataset oficial SUBE 2025](https://datos.transporte.gob.ar/dataset/sube-cantidad-de-transacciones-usos-por-fecha/archivo/ca479a48-1ade-40c3-9681-933f5e644bb3)
- [Feriados Nager.Date API](https://date.nager.at/Api)
- [Feriados La Nación año 2024](https://www.lanacion.com.ar/feriados/2024/)
- [Feriados La Nación año 2025](https://www.lanacion.com.ar/feriados/2025/)

---

## 👨‍💻 Integrantes Grupo 4

- Fica Millán, Yesica  
- Petraroia, Franco  
- Miranda Charca, Florencia  
- De Los Ríos, Raúl  