from selenium import webdriver
import time
import datetime
from openpyxl import load_workbook
import yfinance as yf
from bs4 import BeautifulSoup
import requests

#Preparo la fecha para usar despues
today = datetime.datetime.now()

#Datos de usuario para usar luego.
usuario = "INGRESARUSUARIO"
pw = "INGRESARCONTRASEÑA"


#Iniciar pagina web, cargar credenciales y extraer valor de cartera
driver = webdriver.Chrome('.\chromedriver.exe')
driver.get('https://www.bullmarketbrokers.com/Home/ExclusivePage?url=http%3A%2F%2Fwww.bullmarketbrokers.com%2Fclients%2Fdashboard%2F')
time.sleep(2)

mBox = driver.find_element_by_xpath('//*[@id="txt_login_idNumber"]')
mBox.send_keys(usuario)
mBox = driver.find_element_by_xpath('//*[@id="txt_login_password"]')
mBox.send_keys(pw)

driver.find_element_by_xpath('//*[@id="btn_login_ok"]').click()

time.sleep(4)

ValorCarteraARS = driver.find_element_by_xpath('//*[@id="div_home_index"]/div[1]/div[5]/div[1]/h3[2]')
ValorCartera = ValorCarteraARS.text[3:]
ValorCartera = ValorCartera.replace('.', '')
ValorCartera = ValorCartera.replace(',', '.')

#Agregar datos de indices y dolar
def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

SP = get_current_price('^GSPC')
Nasdaq = get_current_price('^IXIC')
DowJones = get_current_price('^DJI')

url = 'https://dolarhoy.com/cotizacion-dolar-blue'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

blue = soup.find_all('div', class_="value")
dolar = list()
for i in blue:
    dolar.append(i.text)
DolarBlue = dolar[1][1:]

#Cargar datos a excel
ruta = "./prueba.xlsx"
wb = load_workbook(ruta)
sheet = wb.active

datos = [today.strftime("%Y-%m-%d"), float(ValorCartera), float(SP),
         float(Nasdaq), float(DowJones), float(DolarBlue)]
sheet.append(datos)
wb.save(ruta)

#Cierro la conexión a internet
driver.quit()
