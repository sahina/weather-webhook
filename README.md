# Weather forecast wehbook

Webhook for returning weather forecast for date and time used by Google dialogflow bot.

## Requirements

* Api key from `https://openweathermap.org/`
* Set api key to `API_KEY` env variable

## Instructions

This is python 3.7 project.

```
// python deps
pipenv --python 3
pipenv install
pipenv install --dev

// run the app locally
pipnev run python ./weather.py
```

When you run locally, you need to make your public facing api and port accessible via tool like `https://ngrok.com/`

## Deploy

For easy from bot to this webbook, deploy app to a public host like `heroku`