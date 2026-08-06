from playwright.sync_api import sync_playwright
import json
import re
from  datetime import datetime
import pandas as pd

lista=[]

def intercept_response(response):

    if "batchexecute" in response.request.url:
        mostrarData(response.text())

    return response

def mostrarData(raw_text):
    if raw_text.startswith(")]}'"):

        start_idx = raw_text.find("[[")
        if start_idx != -1:
            clean_text = raw_text[start_idx:]
     
            #print("________")
            fin_idx=clean_text.find("generic")
            fin_idx=clean_text.find("]]",fin_idx+7)
            clean_text = clean_text[:fin_idx+2]
            
            #print("_"*20)
            outer_data = json.loads(clean_text)
            
            inner_json_str = outer_data[0][2]
            reviews_list = json.loads(inner_json_str)
            
            for review in reviews_list[0]:

                usuario = review[1][0]
                rating = review[2]
                comentario = review[4]

                timestamp_segundos = review[5][0]
                fecha_legible = datetime.fromtimestamp(timestamp_segundos).strftime('%Y-%m-%d %H:%M:%S')
                
                version_app = review[10] if review[10] else "No especificada"
                
                lista.append({"Usuario":usuario,"Nota":rating,"Comentario":comentario,"Fecha":fecha_legible,"Version":version_app})
                print(f"Usuario: {usuario} | Nota: {rating}⭐")
                print(f"Opinión: {comentario}")
                print(f"Fecha: {fecha_legible}")
                print(f"version app: {version_app}")
                print("-" * 40)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Set the custom user agent when creating a new context
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    page.on("response", intercept_response)

    page.goto("https://play.google.com/store/apps/details?id=com.bcp.innovacxion.yapeapp&hl=es_PE")

    boton_opiniones = page.get_by_text("Ver todas las opiniones", exact=True)
    boton_opiniones.click()


    page.wait_for_timeout(2000)
    page.locator("#sortBy_1").click()
    page.wait_for_timeout(500)

    opcion_reciente = page.locator("span").get_by_text("Más recientes", exact=True)
    opcion_reciente.click()
    page.wait_for_timeout(1000)

    contenedor = page.locator('div[jsname="bN97Pc"]')
    ultima_altura = 0

    try:

        while True:
            altura_actual = contenedor.evaluate("el => el.scrollHeight")
            
            if altura_actual == ultima_altura:
                print("Contenido completamente cargado.")
                break
            if len(lista)>50:
                break;
            ultima_altura = altura_actual
            contenedor.evaluate("el => el.scrollTop = el.scrollHeight")
            page.wait_for_timeout(2500)
    except Exception as e:
        print("Error",str(e))

    df = pd.DataFrame(lista)
    df.to_excel("Data_YAPE.xlsx",index=False)
    print("termino de generar excel")
    browser.close()
