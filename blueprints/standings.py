from flask import Blueprint, request, Response
import requests
import fastf1 as ff1

standings = Blueprint('standings', __name__, template_folder='blueprints')

@standings.route('/standings')
def getStandings():
    reqSeason = request.args.get('season')

    if not reqSeason:
        url = "https://ergast.com/api/f1/current/driverStandings.json"
    else:
        year = int(reqSeason)
        url = "https://ergast.com/api/f1/{}/driverStandings.json".format(year)
        
    response = requests.get(url)
    data = response.json()
    drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'] 
    return drivers_standings