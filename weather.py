import json
import os
import requests
from typing import Dict

from flask import Flask, request, make_response

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "")


@app.route('/webhook', methods=['POST'])
def webhook():
    # incoming request
    print("=== incoming request")
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req))
    print("===")

    # call open weather api
    res = makeResponse(req)
    res = json.dumps(res)

    response = make_response(res)
    response.headers['Content-Type'] = 'application/json'

    return response


def simplify_date(date: str) -> str:
    """Splits date time and return YYYY-MM-DD formatted string"""

    return date.split("T")[0]


def url_for_city(city) -> str:
    """Build open map api url for 5 day forecast for given city"""

    return f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'


def query(city: str, date: str) -> Dict:
    date = simplify_date(date)
    url = url_for_city(city)
    json_object = requests.get(url).json()

    weather = json_object['list']
    forecast = "unknown..."

    date = date.split("T")[0]
    for i in range(0, 30):
        if date in weather[i]['dt_txt']:
            forecast = weather[i]['weather'][0]['description']
            break
    return {
        'city': city,
        'date': date,
        'forecast': forecast,
    }


def makeResponse(req) -> Dict:
    """Calls open weather api for forecast"""

    result = req.get('queryResult')
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = simplify_date(parameters.get('date'))

    response = query(city, date)
    weather = response['forecast']

    speech = f'The forecast for {city} in {date} is {weather}'

    return {
        'source': 'whipdata-weather-webhook',
        'fulfillmentText': speech,
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app at port: ${port}')
    app.run(debug=False, port=port, host='0.0.0.0')
