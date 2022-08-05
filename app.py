from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import fastf1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

fastf1.Cache.enable_cache("./datacache")
fastf1.get_event_schedule(2022)

# Loads weekend into cache

@app.route('/')
def index():
    return "Formula 1 Telemetry API"

@app.route('/grandprix')
def getGrandPrix():
    year = int(request.args.get('year'))
    round = int(request.args.get('round'))
    fastf1.get_session(year, round, "FP1").load()
    fastf1.get_session(year, round, "FP2").load()

    try:
        fastf1.get_session(year, round, "FP3").load()
    except:
        fastf1.get_session(year, round, "S").load()

    fastf1.get_session(year, round, "Q").load()
    fastf1.get_session(year, round, "R").load()

    return "Loading weekend " + str(year) + " round " + str(round)



if __name__=="__main__":
    app.run(debug=True)