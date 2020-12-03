from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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




CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')


options = Options()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.headless = True

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH , chrome_options=options)


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
	}
]

for source in sourceList:
    print("url: ",source['url'])
    driver.get(source['url'])
    el = driver.find_elements(By.XPATH, '//span[@class="numero ng-binding"]')[1]
    
    value = el.text

    print("count: ",value)
    regex = re.compile('[^0-9]')
    value_int = int(regex.sub('', el.text))

    values = Data(value, value_int, source['name'], source['type'])
    db.session.add(values)
    db.session.commit()
    

