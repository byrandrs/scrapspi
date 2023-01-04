import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from urllib import request
import requests
import pandas as pd

url="https://sts.dnp.gov.co/login.aspx?ReturnUrl=%2f%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fspi.dnp.gov.co%252f%26wctx%3drm%253d0%2526id%253dpassive%2526ru%253d%25252f%26wct%3d2022-12-07T16%253a46%253a59Z&wa=wsignin1.0&wtrealm=https%3a%2f%2fspi.dnp.gov.co%2f&wctx=rm%3d0%26id%3dpassive%26ru%3d%252f&wct=2022-12-07T16%3a46%3a59Z"
driver = webdriver.Chrome('./chromedriver')
driver.get(url)


btn_user_ano=driver.find_element("xpath",'//*[@id="linkAnonymousUser"]')
btn_user_ano.click()
btn_consulta=driver.find_element("xpath",'//*[@id="MenuSuperior2_Repeater1_Label1_0"]')
btn_consulta.click()
btn_entidad=driver.find_element("xpath",'//*[@id="Menu1_Repeater1_Label1_2"]')
btn_entidad.click()
btn_porentidad=driver.find_element("xpath",'//*[@id="Menu1_Repeater1_Repeater2_2_HyperLink1_0"]')
btn_porentidad.click()
select = Select(driver.find_element("xpath",'//*[@id="ContentPlaceHolder1_cboSector"]'))
select.select_by_visible_text("Registraduría")
time.sleep(5)
select1=Select(driver.find_element("xpath",'//*[@id="ContentPlaceHolder1_cboEntidad"]'))
select1.select_by_visible_text("FONREGISTRADURIA - FONDO ROTATORIO DE LA REGISTRADURIA")
btn_search=driver.find_element("xpath",'//*[@id="ContentPlaceHolder1_imgBuscar"]')
btn_search.click()
time.sleep(5)

print("Llego a la consulta 1.....")


table1=driver.find_element("xpath",'//*[@id="ContentPlaceHolder1_grvResultados"]')


rows=table1.find_elements(By.TAG_NAME, "tr")

categoria=[]
no_proyectos=[]
inversion=[]
av_financiero=[]
av_fis_producto=[]
av_gestion=[]
del rows[0]

for x in range(0,len(rows)):
    print(x)
    i=rows[x].find_elements(By.TAG_NAME,"td")
    categoria.append(i[0].text)
    no_proyectos.append(i[1].text)
    inversion.append(i[2].text)
    av_financiero.append(i[3].text)
    av_fis_producto.append(i[4].text)
    av_gestion.append(i[5].text)

dc1={'categoria': categoria, 'no_proyectos': no_proyectos, 'inversion': inversion, 'av_financiero': av_financiero, 'av_fis_producto': av_fis_producto, 'av_fis_producto': av_fis_producto,'av_gestion': av_gestion} 
df1=pd.DataFrame(dc1)
print(df1)

table2=driver.find_element("xpath",'//*[@id="ContentPlaceHolder1_GraficaEvolucionFyGEntidad_TablaDatos"]')
rows2=table2.find_elements(By.TAG_NAME, "tr")

mes=[]
inversion=[]
av_financiero=[]
av_fis_producto=[]
av_gestion=[]

for x in range(0,len(rows2)):
    i=rows2[x].find_elements(By.TAG_NAME,"td")
    if x==0:
        for n in range(1,len(i)):
            mes.append(i[n].text)
    if x==1:
        for n in range(1,len(i)):
            inversion.append(i[n].text)
    if x==2:
        for n in range(1,len(i)):
            av_financiero.append(i[n].text)
    if x==3:
        for n in range(1,len(i)):
            av_fis_producto.append(i[n].text)
    if x==4:
        for n in range(1,len(i)):
            av_gestion.append(i[n].text)

dc2={'mes': mes, 'inversion': inversion, 'av_financiero': av_financiero, 'av_fis_producto': av_fis_producto, 'av_gestion': av_gestion} 
df2=pd.DataFrame(dc2)
print(df2)

