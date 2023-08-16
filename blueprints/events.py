from flask import Blueprint, request, Response
import fastf1 as ff1
from fastf1.ergast import Ergast
import pandas as pd
import json
import datetime
import requests
import logging

from flask import Flask

app = Flask(__name__)
events = Blueprint("events", __name__, template_folder="blueprints")
ergast = Ergast(result_type="pandas", auto_cast=True)


@events.route("/grandprix")
def getGrandPrixInfo():
    year = request.args.get("year")
    round = request.args.get("round")
    name = request.args.get("name")

    qualiResults = None
    sprintResults = None
    raceResults = None
    wdcStandings = None
    wccStandings = None

    if name:
        try:
            event = ff1.get_event(int(year), name)
            currentDate = datetime.datetime.now()

            if event.Session4DateUtc < currentDate:
                if event.EventFormat == "conventional":
                    qualiResults = ergast.get_qualifying_results(
                        int(year), event.RoundNumber
                    )
                else:
                    sprintResults = ergast.get_sprint_results(
                        int(year), event.RoundNumber
                    )
            if event.Session5DateUtc < currentDate:
                raceResults = ergast.get_race_results(int(year), event.RoundNumber)

            if event.Session5DateUtc < currentDate:
                wdcStandings = ergast.get_driver_standings(int(year), event.RoundNumber)
                wccStandings = ergast.get_constructor_standings(
                    int(year), event.RoundNumber
                )
            else:
                wdcStandings = ergast.get_driver_standings("current")
                wccStandings = ergast.get_constructor_standings("current")
        except:
            return Response("Grand Prix not found", status=404)
    else:
        try:
            event = ff1.get_event(int(year), int(round))
        except:
            return Response("Grand Prix not found", status=404)

    seriesToJson = event.to_json()
    parsedEvent = json.loads(seriesToJson)

    if qualiResults:
        parsedEvent["qualifyingResults"] = json.loads(
            qualiResults.content[0].to_json(orient="records")
        )
    if sprintResults:
        parsedEvent["sprintResults"] = json.loads(
            sprintResults.content[0].to_json(orient="records")
        )
    if raceResults:
        parsedEvent["raceResults"] = json.loads(
            raceResults.content[0].to_json(orient="records")
        )
    if wdcStandings:
        parsedEvent["wdcStandings"] = json.loads(
            wdcStandings.content[0].to_json(orient="records")
        )
    if wccStandings:
        parsedEvent["wccStandings"] = json.loads(
            wccStandings.content[0].to_json(orient="records")
        )

    return json.dumps(parsedEvent, indent=4)


@events.route("/racecalendar")
def getYearlySchedule():
    year = int(request.args.get("year"))
    includeAll = request.args.get("includeAll") == "true"

    seasons = []
    try:
        mainSeason = ff1.get_event_schedule(year).to_json(orient="records")
        seasons.append({"year": year, "events": json.loads(mainSeason)})
    except:
        return Response("Data not found", status=404)

    if includeAll:
        for i in range(year + 1, datetime.datetime.now().year + 1):
            try:
                additionalSeason = (ff1.get_event_schedule(i)).to_json(orient="records")
                seasons.append({"year": i, "events": json.loads(additionalSeason)})
            except:
                return Response("Data not found for year {}".format(i), status=404)

    return json.dumps(seasons, indent=4)


@events.route("/session")
def getSessionInfo():
    year = int(request.args.get("year"))
    round = int(request.args.get("round"))
    session = int(request.args.get("session"))
    try:
        session = ff1.get_session(year, round, session)
        session.load()
    except:
        return Response("Session not found", status=404)

    result = {
        "results": json.loads(session.results.to_json(orient="records")),
        "laps": json.loads(session.laps.to_json(orient="records")),
    }

    return result


@events.route("/lap")
def getLapInfo():
    year = int(request.args.get("year"))
    round = int(request.args.get("round"))
    session = int(request.args.get("session"))
    driver = request.args.get("driver")
    lap = int(request.args.get("lap"))

    try:
        session = ff1.get_session(year, round, session)
        session.load()
    except:
        return Response("Session not found", status=404)

    try:
        driverLaps = session.laps.pick_driver(driver)
        lapData = driverLaps[driverLaps["LapNumber"] == lap].iloc[0]
    except:
        return Response(
            "No data for driver {} in round {} of {} for lap {}".format(
                driver, round, year, lap
            ),
            status=400,
        )

    carData = lapData.get_car_data().add_distance()

    return carData.to_json(orient="records")


@events.route("/classification")
def getClassification():
    year = int(request.args.get("year"))
    round = int(request.args.get("round"))
    session = int(request.args.get("session"))
    try:
        session = ff1.get_session(year, round, session)
        session.load()
    except:
        return Response("Session not found", status=404)

    url = "https://ergast.com/api/f1/{}/{}/driverStandings.json".format(year, round)
    response = requests.get(url)
    data = response.json()
    drivers_standings = data["MRData"]["StandingsTable"]["StandingsLists"][0][
        "DriverStandings"
    ]

    return {
        "classification": json.loads(session.results.to_json(orient="records")),
        "standings": drivers_standings,
    }


@events.route("/race-classification")
def getRaceClassification():
    year = int(request.args.get("year"))
    round = request.args.get("round")

    if not round:
        round = "last"
    else:
        round = int(round)

    try:
        classification = ergast.get_race_results(year, round)
    except:
        return Response("Classification not found", status=404)

    return classification.content[0].to_json(orient="records")


@events.route("/standings")
def getStandings():
    year = int(request.args.get("year"))
    round = request.args.get("round")

    if not round:
        round = "last"
    else:
        round = int(round)

    try:
        wdcStandings = ergast.get_driver_standings(year, round)
        wccStandings = ergast.get_constructor_standings(year, round)

    except:
        return Response("Standings not found", status=404)

    response = {}
    response["wdc"] = json.loads(wdcStandings.content[0].to_json(orient="records"))

    if len(wccStandings.content) > 0:
        response["wcc"] = json.loads(wccStandings.content[0].to_json(orient="records"))

    return response
