import json
import os
import requests

from flask import Flask, request, make_response

app = Flask(__name__)


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


def query(city, date):
    API_KEY = os.environ.get("API_KEY", "")

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    print("URL:", url)

    json_object = requests.get(url).json()

    print("=== api respose")
    print(json_object)
    print("===")

    weather = json_object['list']
    for i in range(0, 30):
        if date in weather[i]['dt_txt']:
            forecast = weather[i]['weather'][0]['description']
            break
    return {
        'city': city,
        'date': date,
        'forecast': forecast,
    }


def makeResponse(req):
    """Calls open weather api for forecast"""

    result = req.get('queryResult')
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = parameters.get('date')

    response = query(date, city)
    weather = response['forecast']

    speech = f'The forecast for ${city} for ${date} is ${weather}'

    return {
        'source': 'whipdata-weather-webhook',
        'fulfillmentText': speech,
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app at port: ${port}')
    app.run(debug=False, port=port, host='0.0.0.0')
