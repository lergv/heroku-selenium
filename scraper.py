from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

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




CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')


options = Options()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.headless = True




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
		'url':'https://www.bezrealitky.cz/vyhledat#offerType=prodej&estateType=byt&disposition=&ownership=&construction=&equipped=&balcony=&order=timeOrder_desc&boundary=%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B14.2244355%2C50.1029963%5D%2C%5B14.2265265%2C50.1003919%5D%2C%5B14.2328865%2C50.1022635%5D%2C%5B14.2369525%2C50.1010259%5D%2C%5B14.2498381%2C50.1034693%5D%2C%5B14.2583441%2C50.0993837%5D%2C%5B14.2546624%2C50.0986609%5D%2C%5B14.2544382%2C50.097063%5D%2C%5B14.2609996%2C50.0962906%5D%2C%5B14.2610944%2C50.0870952%5D%2C%5B14.2682714%2C50.0857469%5D%2C%5B14.273347%2C50.087619%5D%2C%5B14.2752539%2C50.0810719%5D%2C%5B14.2845716%2C50.0814296%5D%2C%5B14.2850094%2C50.0782609%5D%2C%5B14.2893735%2C50.0771366%5D%2C%5B14.2901916%2C50.073178%5D%2C%5B14.2824327%2C50.0743046%5D%2C%5B14.2772618%2C50.072986%5D%2C%5B14.2785556%2C50.0709193%5D%2C%5B14.2753003%2C50.0730871%5D%2C%5B14.2580521%2C50.0715166%5D%2C%5B14.2587145%2C50.0644236%5D%2C%5B14.2475584%2C50.0622236%5D%2C%5B14.2480852%2C50.0583091%5D%2C%5B14.2508469%2C50.0567694%5D%2C%5B14.2555965%2C50.0570871%5D%2C%5B14.2572299%2C50.0544227%5D%2C%5B14.262304%2C50.0555304%5D%2C%5B14.2643067%2C50.0523325%5D%2C%5B14.2716323%2C50.0543186%5D%2C%5B14.2726358%2C50.0506112%5D%2C%5B14.2681736%2C50.0486908%5D%2C%5B14.2710433%2C50.0469324%5D%2C%5B14.2698804%2C50.0433626%5D%2C%5B14.2686422%2C50.0433361%5D%2C%5B14.2700997%2C50.040097%5D%2C%5B14.2741417%2C50.0357181%5D%2C%5B14.2872209%2C50.0279596%5D%2C%5B14.2975722%2C50.0235558%5D%2C%5B14.3003188%2C50.0246487%5D%2C%5B14.3158709%2C50.0235953%5D%2C%5B14.3165362%2C50.0199126%5D%2C%5B14.3149045%2C50.0143728%5D%2C%5B14.3126082%2C50.0129442%5D%2C%5B14.3114577%2C50.006978%5D%2C%5B14.3064277%2C50.0079528%5D%2C%5B14.3007933%2C50.0118141%5D%2C%5B14.30053%2C50.0043801%5D%2C%5B14.2948377%2C50.0022104%5D%2C%5B14.301838%2C49.9999485%5D%2C%5B14.301036%2C49.9977892%5D%2C%5B14.306243%2C49.997556%5D%2C%5B14.3101029%2C49.993838%5D%2C%5B14.3139615%2C49.9947829%5D%2C%5B14.3181009%2C49.9888928%5D%2C%5B14.3349813%2C49.9938483%5D%2C%5B14.3427557%2C49.9906305%5D%2C%5B14.3353153%2C49.9886648%5D%2C%5B14.3350923%2C49.9864439%5D%2C%5B14.3389488%2C49.9854983%5D%2C%5B14.3375852%2C49.982391%5D%2C%5B14.3395903%2C49.9807517%5D%2C%5B14.3323415%2C49.9773055%5D%2C%5B14.3326071%2C49.9758814%5D%2C%5B14.329934%2C49.9754163%5D%2C%5B14.3302089%2C49.9741785%5D%2C%5B14.3268139%2C49.9718584%5D%2C%5B14.3274645%2C49.9707322%5D%2C%5B14.332299%2C49.9710301%5D%2C%5B14.3406194%2C49.9746139%5D%2C%5B14.3461789%2C49.9747107%5D%2C%5B14.3449986%2C49.9736168%5D%2C%5B14.3470757%2C49.9724752%5D%2C%5B14.344916%2C49.9676279%5D%2C%5B14.3412479%2C49.9657086%5D%2C%5B14.3346987%2C49.9675302%5D%2C%5B14.3292319%2C49.9648505%5D%2C%5B14.3272989%2C49.9632982%5D%2C%5B14.3254392%2C49.9572087%5D%2C%5B14.3343125%2C49.9530497%5D%2C%5B14.3376345%2C49.9483835%5D%2C%5B14.3428774%2C49.9475842%5D%2C%5B14.3587366%2C49.9486837%5D%2C%5B14.3603929%2C49.9474546%5D%2C%5B14.3683756%2C49.9513236%5D%2C%5B14.3716866%2C49.9503234%5D%2C%5B14.373208%2C49.9471224%5D%2C%5B14.3768119%2C49.9466207%5D%2C%5B14.3797583%2C49.9492145%5D%2C%5B14.3879707%2C49.9497837%5D%2C%5B14.3890496%2C49.9451745%5D%2C%5B14.395562%2C49.9419006%5D%2C%5B14.3968649%2C49.9444156%5D%2C%5B14.3942296%2C49.9538976%5D%2C%5B14.4006472%2C49.9706693%5D%2C%5B14.4194183%2C49.9635636%5D%2C%5B14.4277435%2C49.9645%5D%2C%5B14.4302341%2C49.966839%5D%2C%5B14.4386195%2C49.9681197%5D%2C%5B14.4445941%2C49.9738632%5D%2C%5B14.4622402%2C49.9707711%5D%2C%5B14.4625192%2C49.9725303%5D%2C%5B14.4641082%2C49.972691%5D%2C%5B14.4663038%2C49.9810366%5D%2C%5B14.4739923%2C49.9804035%5D%2C%5B14.473704%2C49.9837523%5D%2C%5B14.486985%2C49.985687%5D%2C%5B14.4870376%2C49.9875848%5D%2C%5B14.4845836%2C49.9874152%5D%2C%5B14.4839334%2C49.992419%5D%2C%5B14.5072536%2C49.9974771%5D%2C%5B14.5093561%2C49.9938535%5D%2C%5B14.5075143%2C49.9934731%5D%2C%5B14.5081846%2C49.9921388%5D%2C%5B14.5137466%2C49.992583%5D%2C%5B14.5134214%2C49.9945336%5D%2C%5B14.5179512%2C49.9944175%5D%2C%5B14.5191339%2C49.9971001%5D%2C%5B14.5243223%2C49.9974342%5D%2C%5B14.5300192%2C50.0007153%5D%2C%5B14.520994%2C50.0077216%5D%2C%5B14.5274725%2C50.0108381%5D%2C%5B14.5354842%2C50.011751%5D%2C%5B14.5423599%2C50.0086999%5D%2C%5B14.5508521%2C50.0079867%5D%2C%5B14.5534669%2C50.0094627%5D%2C%5B14.5542318%2C50.0121564%5D%2C%5B14.5627521%2C50.0115863%5D%2C%5B14.5640792%2C50.0097357%5D%2C%5B14.5675263%2C50.0094888%5D%2C%5B14.5683172%2C50.0073516%5D%2C%5B14.582393%2C50.0163634%5D%2C%5B14.5817136%2C50.010951%5D%2C%5B14.5870869%2C50.0114527%5D%2C%5B14.5891623%2C50.008657%5D%2C%5B14.5944084%2C50.0100508%5D%2C%5B14.5949721%2C50.007143%5D%2C%5B14.6022636%2C50.0094315%5D%2C%5B14.6039007%2C50.0019258%5D%2C%5B14.6078305%2C50.002937%5D%2C%5B14.6103406%2C49.9986363%5D%2C%5B14.6134893%2C49.9999981%5D%2C%5B14.6191943%2C49.9975247%5D%2C%5B14.6223474%2C49.9986156%5D%2C%5B14.6291605%2C49.9955374%5D%2C%5B14.6339958%2C49.9961302%5D%2C%5B14.6401518%2C49.9944411%5D%2C%5B14.6469229%2C49.9987546%5D%2C%5B14.6382891%2C50.0057827%5D%2C%5B14.6438141%2C50.0065389%5D%2C%5B14.6454958%2C50.0047342%5D%2C%5B14.6498044%2C50.0087938%5D%2C%5B14.6577854%2C50.0043495%5D%2C%5B14.6626155%2C50.008403%5D%2C%5B14.6615844%2C50.0127835%5D%2C%5B14.6685483%2C50.0134346%5D%2C%5B14.669537%2C50.0188407%5D%2C%5B14.6561272%2C50.0309551%5D%2C%5B14.6569571%2C50.0378173%5D%2C%5B14.6668511%2C50.0385277%5D%2C%5B14.6538674%2C50.0492542%5D%2C%5B14.6479462%2C50.0436683%5D%2C%5B14.6440386%2C50.0421831%5D%2C%5B14.6402196%2C50.0484131%5D%2C%5B14.6413491%2C50.0541306%5D%2C%5B14.6401916%2C50.0568947%5D%2C%5B14.6458266%2C50.0587354%5D%2C%5B14.6448369%2C50.0600564%5D%2C%5B14.652135%2C50.059538%5D%2C%5B14.6514504%2C50.0619535%5D%2C%5B14.6581022%2C50.061066%5D%2C%5B14.6581693%2C50.0622841%5D%2C%5B14.6671358%2C50.0637853%5D%2C%5B14.6747647%2C50.067558%5D%2C%5B14.6908607%2C50.0720182%5D%2C%5B14.6999919%2C50.0721289%5D%2C%5B14.7067867%2C50.0870194%5D%2C%5B14.7039175%2C50.0917426%5D%2C%5B14.6886937%2C50.0963003%5D%2C%5B14.688646%2C50.0988438%5D%2C%5B14.6911961%2C50.0998947%5D%2C%5B14.6903288%2C50.1006277%5D%2C%5B14.6768033%2C50.1016454%5D%2C%5B14.6685944%2C50.103972%5D%2C%5B14.665884%2C50.1026521%5D%2C%5B14.6606212%2C50.1065345%5D%2C%5B14.6574355%2C50.1065009%5D%2C%5B14.6567598%2C50.1098902%5D%2C%5B14.6591154%2C50.1226041%5D%2C%5B14.6352008%2C50.1239183%5D%2C%5B14.6354185%2C50.1263749%5D%2C%5B14.6322995%2C50.1299032%5D%2C%5B14.6086335%2C50.1271149%5D%2C%5B14.6005164%2C50.129523%5D%2C%5B14.5952125%2C50.1339214%5D%2C%5B14.5923328%2C50.138741%5D%2C%5B14.5897331%2C50.1396718%5D%2C%5B14.591358%2C50.1426913%5D%2C%5B14.5877286%2C50.1452435%5D%2C%5B14.5884301%2C50.1471545%5D%2C%5B14.5931774%2C50.1476305%5D%2C%5B14.5934964%2C50.1500718%5D%2C%5B14.5990028%2C50.1541328%5D%2C%5B14.584351%2C50.1536431%5D%2C%5B14.5785323%2C50.1502016%5D%2C%5B14.5687846%2C50.1500378%5D%2C%5B14.5661556%2C50.1516488%5D%2C%5B14.5632297%2C50.1501702%5D%2C%5B14.5604828%2C50.1553647%5D%2C%5B14.5627472%2C50.1560274%5D%2C%5B14.5609936%2C50.1615751%5D%2C%5B14.550447%2C50.164824%5D%2C%5B14.5505391%2C50.1661221%5D%2C%5B14.542381%2C50.1625767%5D%2C%5B14.5403349%2C50.1650878%5D%2C%5B14.5342354%2C50.161565%5D%2C%5B14.5305116%2C50.1661902%5D%2C%5B14.5326164%2C50.1674735%5D%2C%5B14.5313005%2C50.1725034%5D%2C%5B14.5324832%2C50.1771831%5D%2C%5B14.5268551%2C50.1774301%5D%2C%5B14.5195803%2C50.1748765%5D%2C%5B14.5090714%2C50.1741607%5D%2C%5B14.5069039%2C50.1714361%5D%2C%5B14.4795218%2C50.1722942%5D%2C%5B14.4801495%2C50.1698783%5D%2C%5B14.4669127%2C50.1695438%5D%2C%5B14.4667688%2C50.1654264%5D%2C%5B14.4638436%2C50.1648787%5D%2C%5B14.4641231%2C50.159923%5D%2C%5B14.4518653%2C50.1578317%5D%2C%5B14.4366841%2C50.1575069%5D%2C%5B14.4360049%2C50.1590913%5D%2C%5B14.4281375%2C50.1576674%5D%2C%5B14.4289771%2C50.1535113%5D%2C%5B14.4200136%2C50.1529649%5D%2C%5B14.4206908%2C50.1503338%5D%2C%5B14.4225022%2C50.1498332%5D%2C%5B14.4071204%2C50.1469772%5D%2C%5B14.3999734%2C50.1479062%5D%2C%5B14.3991472%2C50.1433746%5D%2C%5B14.3970345%2C50.1435221%5D%2C%5B14.3949016%2C50.141429%5D%2C%5B14.3920497%2C50.1417845%5D%2C%5B14.3911145%2C50.1439606%5D%2C%5B14.3848779%2C50.1469262%5D%2C%5B14.3657001%2C50.1480311%5D%2C%5B14.3560896%2C50.1411726%5D%2C%5B14.357788%2C50.1405714%5D%2C%5B14.3574302%2C50.1392878%5D%2C%5B14.3541236%2C50.137526%5D%2C%5B14.3544189%2C50.1362567%5D%2C%5B14.3561548%2C50.1366347%5D%2C%5B14.3574439%2C50.1296478%5D%2C%5B14.3600421%2C50.1295213%5D%2C%5B14.3556407%2C50.1246523%5D%2C%5B14.3612434%2C50.1178977%5D%2C%5B14.3607835%2C50.1160189%5D%2C%5B14.3276429%2C50.116752%5D%2C%5B14.3206068%2C50.1152415%5D%2C%5B14.3156962%2C50.1229456%5D%2C%5B14.3158782%2C50.1286167%5D%2C%5B14.3103247%2C50.1277719%5D%2C%5B14.3024335%2C50.1300768%5D%2C%5B14.3002026%2C50.1266435%5D%2C%5B14.2946854%2C50.1247846%5D%2C%5B14.2971713%2C50.1205942%5D%2C%5B14.2883495%2C50.1162211%5D%2C%5B14.2846626%2C50.1154697%5D%2C%5B14.2788382%2C50.1190811%5D%2C%5B14.2600445%2C50.1134439%5D%2C%5B14.2571607%2C50.1145639%5D%2C%5B14.2560759%2C50.1125388%5D%2C%5B14.2500356%2C50.1107913%5D%2C%5B14.2451109%2C50.1099769%5D%2C%5B14.2388054%2C50.1117993%5D%2C%5B14.2370135%2C50.1102209%5D%2C%5B14.2393227%2C50.1072816%5D%2C%5B14.2244355%2C50.1029963%5D%5D%5D%7D%7D&center=%5B14.465611099999933%2C50.05980988882612%5D&zoom=9.278406855861746&locationInput=Praha%2C%20Hlavn%C3%AD%20m%C4%9Bsto%20Praha%2C%20%C4%8Cesko&limit=15',
		'type':"bezrealitky_prodej",
                'name':"count"
	}
]

for source in sourceList:

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH , chrome_options=options)
    
    print("url: ",source['url'])
    driver.get(source['url'])
    if (source['type'] == "sreality_pronajem" or source['type'] == "sreality" ):
        el = driver.find_elements(By.XPATH, '//span[@class="numero ng-binding"]')[1]
    if (source['type'] == "bezrealitky_prodej"):
        el = driver.find_elements(By.XPATH, '//span[@class="text-no-break"]')[0]
    value = el.text

    print("count: ",value)
    regex = re.compile('[^0-9]')
    value_int = int(regex.sub('', el.text))

    values = Data(value, value_int, source['name'], source['type'])
    db.session.add(values)
    db.session.commit()
    

