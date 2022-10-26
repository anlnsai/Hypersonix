from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json


app = Flask(__name__)
auth = HTTPBasicAuth()
BASE_URL = "https://api.coingecko.com/api/v3"

users = {
    "test": generate_password_hash("hello"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/list')
@auth.login_required
def index():
    url = BASE_URL + '/coins/list'
    res = requests.get(url= url)
    result = []
    for data in json.loads(res.text):
        temp = {}
        temp['name'] = data['name']
        temp['symbol'] = data['symbol']
        result.append(temp)

    return jsonify(result)


@app.route('/get_price')
@auth.login_required
def details():
    url = BASE_URL + '/coins/markets?vs_currency=usd'
    res = requests.get(url= url)
    result = []
    for data in json.loads(res.text):
        temp = {}
        temp['name'] = data['name']
        temp['current_price'] = data['current_price']
        result.append(temp)

    return jsonify(result)


@app.route('/get_trend')
@auth.login_required
def trend():
    url = BASE_URL + '/search/trending'
    res = requests.get(url= url)
    result = []
    for data in json.loads(res.text)['coins']:
        temp = {}
        temp['name'] = data['item']['name']
        temp['current_price'] = str(data['item']['price_btc']) + "(BTC)"
        result.append(temp)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)