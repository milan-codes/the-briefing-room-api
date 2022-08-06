from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import fastf1
from blueprints.quali import quali
from blueprints.gpinfo import gpinfo

app = Flask(__name__)
app.register_blueprint(quali)
app.register_blueprint(gpinfo)

fastf1.Cache.enable_cache("./datacache")

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