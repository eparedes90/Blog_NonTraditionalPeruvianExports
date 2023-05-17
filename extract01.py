# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:54:18 2023

@author: Eduardo Paredes
"""


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import numpy as np
import time
import pandas as pd

#create the driver
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver_path = 'E://Asesorías de tesis//Economía//exportacionesNoTradicionales2//raw//chromedriver.exe'

#create the list of partidas
list_partidas = ['0810400000',
'0806100000',
'0709200000',
'0804400000',
'0307430000',
'0804502000',
'1605540000',
'0803901100',
'0904201010',
'2005991000',
'2510100000',
'6109100031',
'7113190000',
'6109100039',
'7901120000',
'7408110000',
'2309909000',
'4911100000',
'6204610000',
'6105100041']

#create list of years
years = np.arange(2001, 2023, 1)
years = years.astype(str)
list_years = years.tolist()

#elaborate the loop by years and partidas
list_tables = []

for y in list_years:
    for p in list_partidas:
        
        driver = webdriver.Chrome(driver_path, chrome_options=options)
        driver.get('http://www.aduanet.gob.pe/cl-ad-itestadispartida/resumenPPaisS01Alias?accion=cargarFrmResumenPPais')

        #select the year in web
        year = driver.find_element(By.NAME, value = 'ano_prese')
        temp = Select(year)
        temp.select_by_value(y)
        
        #select the option exports
        driver.find_element(By.XPATH, value = '/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[2]')\
            .click()
        
        #fill with partida
        driver.find_element(By.XPATH, value = '/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]/input')\
            .send_keys(p)
            
        #click en 'consultar'
        driver.find_element(By.XPATH, value = '/html/body/form/table/tbody/tr/td/div/input[1]')\
            .click()
            
        # find the table element using Selenium
        table_element = driver.find_element(By.XPATH, value = "/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table")
        
        # get the HTML code for the table
        table_html = table_element.get_attribute('outerHTML')
        
        #close the driver
        driver.close()
        
        #read the table
        temp = pd.read_html(table_html)
        
        #transform to data frame
        temp = pd.DataFrame(temp[0])
        
        #select columns
        temp = temp[['País de Destino', 'Valor FOB(dólares)', 'Peso Neto(Kilos)',
               'Peso Bruto(Kilos)', 'Porcentaje FOB']]
        
        #add a column for the partida
        temp['Partida'] = p
        
        #add column year
        temp["Año"] = y
        
        list_tables.append(temp)

#concat all the tables of list_tables
df = pd.concat(list_tables, ignore_index=True)

#save as pkl
df.to_pickle("data_extracted\raw_exports.pkl")
