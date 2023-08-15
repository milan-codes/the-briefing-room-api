# The Briefing Room API

[The Briefing Room](https://github.com/milan-codes/the-briefing-room) is a web application designed by a passionate fan of F1. The goal of this app is to provide a platform where fellow enthusiasts can dive into the world of F1 racing through in-depth telemetry data analysis. You can explore historical race data, compare drivers' telemetry, and stay up-to-date with the latest race results and championship standings. This is a simple Flask API that serves the web app. ⚙️

## Tech used

- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- This project wouldn't be possible without the amazing [FastF1](https://github.com/theOehrly/Fast-F1) package

## Getting started

### Prerequisites

1. You'll need to have Python installed (3.x)

### Installation

1. In order to run the web application locally, you need to install and run [The Briefing Room API](https://github.com/milan-codes/the-briefing-room-api).
2. Clone this repository with: `git clone git@github.com:milan-codes/the-briefing-room-api.git`
3. Navigate to the folder and create a directory called `datacache`, which will cache the data received by FastF1: `mkdir datacache`
4. Create a virtual environment for Flask: `python3 -m venv venv`
5. Activate the virtual environment: `source venv/bin/activate` (use the script that'll work with your sell, the available scripts can be seen in `venv/bin`)
6. Install the requirements recursively: `pip3 install requirements.txt`
7. Start the dev server: `python3 app.py`

After stopping the server, you can deactivate the virtual environment by simply typing `deactivate`

## Contributing

Contributions are welcomed! If you have coding skills, insights, or ideas to improve the app, you can actively participate in its development. Whether it's fixing bugs, adding new features, or suggesting improvements, your input can make a significant difference. Open an issue if you have any insights.

- Note that only signed commits are accepted

## Disclaimer

The creator of this web application is in no way, shape or form linked to FORMULA 1, Liberty Media, the FIA or any other organization. This website was created only for fun, and educational purposes and it does not generate any revenue. All rights belong to their respective owners. Any insights or data derived from the app should be regarded as unofficial and for informational purposes only.
