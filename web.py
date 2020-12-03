import os
from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import configparser
import io
import random #defaultne nainstalovany v python 3
#pip install matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import send_file

from matplotlib.dates import DayLocator, HourLocator, DateFormatter, WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
#pip install numpy==1.19.3

config = configparser.ConfigParser()
#config.read('./settings/config_local.ini')


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['STRING']
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


@app.route('/')
def index():
    return render_template("index.html", name="test")

@app.route('/fig/')
def fig():
    fig = create_plot()
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

#2020-11-16 13:56:04.891475+00
def get_data():
    sql_query = """select data.id,
                    date "day",
                    --TO_CHAR(date :: DATE, 'dd/mm/yyyy')"day" ,
                    --date_part('day',date) "day",
                    data.value_int
                    from data
                    where data.id in
                        (select a.max_id from
                            (SELECT
                                date_trunc('day', data.date) "day",
                                count(*),
                                max(data.id) "max_id",
                                max(data.date)
                            FROM data
                            WHERE data.type = 'sreality'
                            group by 1
                            ORDER BY 1) as a
                        )
                        AND data.type = 'sreality'
                        ORDER BY date"""
    result = db.engine.execute(sql_query)
    ys = []
    xs = []
    for r in result:
        ys.append(r['value_int'])
        #xs.append(datetime.strptime(r['day'], '%Y-%m-%d %H:%M:%S.%f'))
        xs.append(r['day'])

    return [xs, ys]

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    result = get_data()
    axis.plot(result[0], result[1])
    fig.autofmt_xdate()
    return fig

def create_plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    result = get_data()
    axis.plot_date(result[0], result[1], 'b-')
    axis.xaxis.set_major_locator(DayLocator(interval=5))
    
    fig.autofmt_xdate()
    return fig


if __name__ == "__main__":
    app.run(debug=True)
