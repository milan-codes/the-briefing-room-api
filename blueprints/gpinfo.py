from flask import Blueprint, request, Response
import fastf1 as ff1
import pandas as pd
import json
import datetime

gpinfo = Blueprint('gpinfo', __name__, template_folder='blueprints')

@gpinfo.route('/grandprix')
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

@gpinfo.route('/racecalendar')
def getYearlySchedule():
    year = int(request.args.get('year'))
    withTelemetry = request.args.get('withTelemetry') == 'true'
    includeAll = request.args.get('includeAll') == 'true'

    try:
        events = ff1.get_event_schedule(year).to_json(orient='records')
    except:
        return Response("Data not found", status=404)

    if includeAll:
        for i in range(year+1, datetime.datetime.now().year + 1):
            try:
                events2 = (ff1.get_event_schedule(i)).to_json(orient='records')
            except:
                return Response("Data not found for year {}".format(i), status=404)

    dictA = {2021: json.loads(events)}
    dictB = {2022: json.loads(events2)}
    return json.dumps({**dictA, **dictB}, indent=4)