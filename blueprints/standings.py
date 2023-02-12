from flask import Blueprint, request, Response
import requests
import fastf1 as ff1

standings = Blueprint('standings', __name__, template_folder='blueprints')

@standings.route('/standings')
def getStandings():
    reqYear = request.args.get('year')
    reqRound = request.args.get('round')

    if not reqYear or not reqRound:
        url = "https://ergast.com/api/f1/current/driverStandings.json"
    else:
        year = int(reqYear)
        round = int(reqRound)
        url = "https://ergast.com/api/f1/{}/{}/driverStandings.json".format(year, round)
        
    response = requests.get(url)
    data = response.json()
    drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'] 
    return drivers_standings