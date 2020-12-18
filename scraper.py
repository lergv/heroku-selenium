from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os
import configparser
config = configparser.ConfigParser()
#config.read('./settings/config_local.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(300))
    type = db.Column(db.String(100))
    value_int = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, value, value_int, name, type):
        self.value = value
        self.value_int = value_int
        self.name = name
        self.type = type
        
    def __repr__(self):
        return "<Data(value='%s', value_int='%s', name='%s', type='%s', date='%s')>" % (self.value, self.value_int, self.name, self.type, self.date)




#CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
#CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', r'D:/git/scraping/webdriver/chromedriver.exe')

#GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')
#GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', r'D:/git/scraping/webdriver/chromedriver.exe')


##options = Options()
##options.binary_location = GOOGLE_CHROME_BIN
##options.add_argument('--disable-gpu')
##options.add_argument('--no-sandbox')
##options.headless = True
##prefs = {"profile.managed_default_content_settings.images": 2}
##

options = Options()
options.add_argument("start-maximized"); # open Browser in maximized mode
options.add_argument("disable-infobars"); # disabling infobars
options.add_argument("--disable-extensions"); # disabling extensions
options.add_argument("--disable-gpu"); # applicable to windows os only
options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
options.add_argument("--no-sandbox"); # Bypass OS security model
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

sourceList = [
	{
		'url':'https://www.sreality.cz/hledani/prodej/byty/praha',
		'type':"sreality",
                'name':"count"
	},
	{
		'url':'https://www.sreality.cz/hledani/pronajem/byty/praha',
		'type':"sreality_pronajem",
                'name':"count"
	},
	{
		'url':'https://reality.idnes.cz/s/prodej/byty/praha',
		'type':"idnes_prodej",
                'name':"count"
	}
]

for source in sourceList:

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH , chrome_options=options)
    
    print("url: ",source['url'])
    driver.get(source['url'])
    if (source['type'] == "sreality_pronajem" or source['type'] == "sreality" ):
        el = driver.find_elements(By.XPATH, '//span[@class="numero ng-binding"]')[1]
##    if (source['type'] == "bezrealitky_prodej"):
##        timeout = 60
##        try:
##            element_present = EC.presence_of_element_located((By.XPATH, 'span[@class="text-no-break"]'))
##            WebDriverWait(driver, timeout).until(element_present)
##        except TimeoutException:
##            print("Timed out waiting for page to load")
##        finally:
##            print("Page loaded")
##            el = driver.find_elements(By.XPATH, '//*')[0]
##            print(el)
    if (source['type'] == "idnes_prodej"):
        el = driver.find_elements(By.XPATH, '//p[@class="mb-10 h3 font-regular pull-t-left"]')[0]


    value = el.text

    print("count: ",value)
    regex = re.compile('[^0-9]')
    value_int = int(regex.sub('', el.text))

    values = Data(value, value_int, source['name'], source['type'])
    db.session.add(values)
    db.session.commit()
    

