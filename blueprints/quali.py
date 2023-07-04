from flask import Blueprint, request, Response
import fastf1 as ff1
import json
import pandas as pd

quali = Blueprint('quali', __name__, template_folder='blueprints')

@quali.route('/qualilap')
def getLapTelemetryVelocity():
    year = int(request.args.get('year'))
    round = int(request.args.get('round'))
    driver = request.args.get('driver')
    lap = request.args.get('lap')
    isFastestLap = False if isinstance(lap, int) else True

    try:
        session = ff1.get_session(year, round, "Q")
        session.load()
    except:
        return Response("Session not found", status=404)

    try:
        driverLaps = session.laps.pick_driver(driver)
        lapData = driverLaps.pick_fastest() if isFastestLap else driverLaps[driverLaps['LapNumber'] == int(lap)].iloc[0]
    except:
        return Response("No data for driver {} in round {} of {} for lap {}".format(driver, round, year, lap), status=400)
    
    print(lapData)
    carData = lapData.get_car_data()
    time = carData['Time']
    velocity = carData['Speed']

    timeDataFrameToJson = time.to_json()
    timeParsed = json.loads(timeDataFrameToJson)
    velocityDataFrameToJson = velocity.to_json()
    velocityParsed = json.loads(velocityDataFrameToJson)
    return json.dumps({'time': timeParsed, 'velocity': velocityParsed}, indent=4)