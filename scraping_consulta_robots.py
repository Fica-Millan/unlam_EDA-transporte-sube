import requests

# Consulta el archivo robots.txt del sitio de Wikipedia
print(requests.get("https://www.lanacion.com.ar/robots.txt").text)

'''
El archivo nO prohíbe de forma general el scraping. 
⛔ Solo restringe el acceso a ciertas rutas, como: 
- /sinbarreras, /newsletters/, /registracion, etc.
- URLs con ?utm_* en los parámetros.
- Algunas rutas específicas como /buscador, /pf/api/..., y ciertos artículos puntuales.

# 👉🏼 La página de feriados https://www.lanacion.com.ar/feriados/2024/ no está bloqueada
# ✅ Se puede hacer scraping de esa página.
'''