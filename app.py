from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
import fastf1
from blueprints.quali import quali
from blueprints.events import events
from blueprints.standings import standings

app = Flask(__name__)
CORS(app)
app.register_blueprint(quali)
app.register_blueprint(events)
app.register_blueprint(standings)

fastf1.Cache.enable_cache("./datacache")

@app.route('/')
def index():
    return "The Briefing Room API"

if __name__=="__main__":
    app.run(debug=True)