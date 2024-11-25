# Funciones relacionadas con la extracción de datos.# scraper.py
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import time
import pandas as pd
import random
from table import create_dataframe

def create_driver():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')  # Para ejecutar sin abrir ventana
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Cambiar el User-Agent
    # Instalar y configurar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=option)


def get_data_from_page(DNI):
    retries = 3
    attempt = 0
    while attempt < retries:
        try:
            # Crear el controlador
            driver = create_driver()    
            driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')

            # Esperar a que los elementos estén disponibles
            Wait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btnPorDocumento'))
            ).click()

            # Ingresar el DNI
            Wait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'txtNumeroDocumento'))
            ).send_keys(DNI)

            # Hacer clic en "Aceptar"
            driver.find_element(By.ID, 'btnAceptar').click()

            # Esperar a que los elementos de la consulta aparezcan
            Wait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item-heading'))
            )

            # Extraer los datos de las etiquetas h4, p y small
            h4_elements = driver.find_elements(By.CLASS_NAME, 'list-group-item-heading')
            p_elements = driver.find_elements(By.CLASS_NAME, 'list-group-item-text')
            small_elements = driver.find_elements(By.TAG_NAME, 'small')

            # Almacenar los textos en listas
            h4_texts = [h4.text for h4 in h4_elements]
            p_texts = [p.text for p in p_elements]
            small_texts = [small.text for small in small_elements]

            # Primera tabla de consulta
            df_1 = create_dataframe(h4_texts, p_texts, small_texts)

            Wait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.list-group-item.clearfix.aRucs'))
            ).click()

            h4_elements_2 = Wait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item-heading')))

            p_elements_2 = Wait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item-text')))

            td_elements = Wait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//td")))

            p_elements_3 = Wait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '/html/body/div/div[2]/div/div[3]/div[2]/div[14]/div/div[2]')))

            # Verificar si ocurre un error, como cuando no se encuentra un RUC
            try:
                error_message = Wait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "strong"))
                ).text
                
                # Si se encuentra el mensaje de error, indicamos que no hay RUC para ese DNI
                if 'El Sistema RUC NO REGISTRA un número de RUC' in error_message:
                    print(f"El DNI {DNI} no tiene RUC asociado.")
                    driver.close()
                    return None, None  # Devolver None si no hay RUC

            except:
                # Si no hay mensaje de error, continuamos con la extracción de datos
                pass

            # Ahora obtenemos las listas de texto para las siguientes partes
            td_texts = [td.text.strip() for td in td_elements if td.text.strip() != '']
            h4_texts_2 = [h4.text for h4 in h4_elements_2][2:]
            p_texts_2 = [p.text for p in p_elements_2]
            p_texts_3 = [element.text.strip() for element in p_elements_3]

            # Limpiar el texto cuando contiene un mensaje específico
            def clean_baja_de_oficio(p_texts):
                mensaje_baja = "IMPORTANTE: Los comprobantes de pago o notas de débito emitidos por este contribuyente no dan derecho a crédito fiscal del IGV, en tanto se encuentra con estado de BAJA DE OFICIO"
                
                if p_texts and p_texts[0] == mensaje_baja:
                    p_texts = p_texts[1:]
                if p_texts and p_texts[-1] == mensaje_baja:
                    p_texts = p_texts[:-1]

                return p_texts

            p_texts_2 = clean_baja_de_oficio(p_texts_2)

            # Insertar datos adicionales
            p_texts_2.insert(11, td_texts[0])
            p_texts_2.insert(12, td_texts[1])
            p_texts_2.insert(17, td_texts[2])

            if p_texts_3:
                p_texts_2.insert(13, p_texts_3[0])

            # Crear el segundo DataFrame
            df_2 = pd.DataFrame([p_texts_2], columns=h4_texts_2)

            # Cerrar el navegador
            time.sleep(5)
            driver.close()

            return df_1, df_2

        except Exception as e:
            print(f'Error procesando el DNI {DNI}, reintentando... {str(e)}')
            attempt +=1
            time.sleep(random.uniform(3,7))

    # Si no conseguimos datos después de reintentos, regresamos None
    print(f"Error al procesar el DNI {DNI} después de {retries} intentos.")
    return None, None
