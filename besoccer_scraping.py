# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 10:27:21 2025

@author: Jorge Acín Zurita
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Iniciar Selenium con Firefox
driver = webdriver.Firefox()
driver.set_window_size(1280, 900)

# Abrir la página del jugador
driver.get('https://es.besoccer.com/jugadores')
driver.implicitly_wait(3)

# Aceptar cookies si aparecen
try:
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "css-5fw3i6"))
    ).click()
except:
    print("No se encontró el botón de cookies o ya fue aceptado.")

# Buscar al jugador
buscador_besocc = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "search-input"))
)
buscador_besocc.click()
buscador_besocc.send_keys("Marcus Rashford")
time.sleep(2)
buscador_besocc.send_keys(Keys.ENTER)

# Esperar la carga de la página de resultados y seleccionar el primer jugador encontrado
try:
    jugador = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/jugador/')]"))
    )
    jugador.click()
except:
    print("No se encontró el jugador en los resultados.")
    driver.quit()
    exit()

# Esperar la carga de la página del jugador
time.sleep(3)

# Buscar el gráfico de evolución del mercado
try:
    grafico = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "player-market"))
    )
except:
    print("No se encontró el gráfico de evolución del mercado.")
    driver.quit()
    exit()

# Hacer scroll al gráfico
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", grafico)
time.sleep(2)

# Buscar los puntos en el gráfico
puntos = grafico.find_elements(By.TAG_NAME, "circle")
print(f"Se encontraron {len(puntos)} puntos en el gráfico.")

punto_2022 = None
for punto in puntos:
    try:
        cx_value = float(punto.get_attribute("cx"))
        if 300 < cx_value < 320:  # Rango aproximado para el año 2022
            punto_2022 = punto
            break
    except:
        continue

if not punto_2022:
    print("No se encontró un punto correspondiente a 2022 en el gráfico.")
    driver.quit()
    exit()

# Mover el cursor sobre el punto
ActionChains(driver).move_to_element(punto_2022).perform()
time.sleep(2)

# Extraer el valor del tooltip
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

tooltip = soup.find("div", style=lambda x: x and "position: absolute" in x)

if tooltip:
    valor_mercado_2022 = tooltip.text.strip()
    print(f"Valor de mercado en 2022: {valor_mercado_2022}")
else:
    print("No se encontró el valor de mercado para 2022.")

# Cerrar Selenium
driver.quit()

