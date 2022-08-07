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

if __name__=="__main__":
    app.run(debug=True)