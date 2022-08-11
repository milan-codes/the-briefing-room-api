from flask import Blueprint, request, Response
import fastf1 as ff1
import pandas as pd
import json
import datetime

events = Blueprint('events', __name__, template_folder='blueprints')

@events.route('/grandprix')
def getGrandPrixInfo():
    year = int(request.args.get('year'))
    round = int(request.args.get('round'))
    try:
        event = ff1.get_event(year, round)
    except:
        return Response("Grand Prix not found", status=404)

    seriesToJson = event.to_json()
    parsedEvent = json.loads(seriesToJson)
    return json.dumps(parsedEvent, indent=4)

@events.route('/racecalendar')
def getYearlySchedule():
    year = int(request.args.get('year'))
    includeAll = request.args.get('includeAll') == 'true'

    seasons = []
    try:
        mainSeason = ff1.get_event_schedule(year).to_json(orient='records')
        seasons.append({ "year": year, "events": json.loads(mainSeason) })
    except:
        return Response("Data not found", status=404)

    if includeAll:
        for i in range(year+1, datetime.datetime.now().year + 1):
            try:
                additionalSeason = (ff1.get_event_schedule(i)).to_json(orient='records')
                seasons.append({ "year": i, "events": json.loads(additionalSeason) })
            except:
                return Response("Data not found for year {}".format(i), status=404)

    return json.dumps(seasons, indent=4)

@events.route("/session")
def getSessionInfo():
    year = int(request.args.get('year'))
    round = int(request.args.get('round'))
    session = int(request.args.get('session'))
    try:
        session = ff1.get_session(year, round, session)
        session.load()
    except:
        return Response("Session not found", status=404)
    
    drivers = session.drivers
    result = {"drivers": drivers, "laps": json.loads(session.laps.to_json(orient='records'))}

    return result

@events.route("/lap")
def getLapInfo():
    year = int(request.args.get('year'))
    round = int(request.args.get('round'))
    session = int(request.args.get('session'))
    driver = int(request.args.get('driver'))
    lap = int(request.args.get('lap'))

    try:
        session = ff1.get_session(year, round, session)
        session.load()
    except:
        return Response("Session not found", status=404)

    try:
        driverLaps = session.laps.pick_driver(driver)
        lapData = driverLaps[driverLaps['LapNumber'] == lap].iloc[0]
    except:
        return Response("No data for driver {} in round {} of {} for lap {}".format(driver, round, year, lap), status=400)
    
    carData = lapData.get_car_data().add_distance()

    return carData.to_json(orient='records')