# backend/app.py

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import random
import json
import threading
import time

app = Flask(__name__)

stocks_data = []

def refresh_stock_price(symbol, refresh_interval):
    while True:
        time.sleep(refresh_interval)
        stock = next((s for s in stocks_data if s['symbol'] == symbol), None)
        if stock:
            stock['price'] += random.uniform(-1, 1)

def fetch_stock_data():
    with open('stocks_data.json', 'r') as file:
        return json.load(file)

def save_stock_data():
    with open('stocks_data.json', 'w') as file:
        json.dump(stocks_data, file)

def initialize_stocks():
    global stocks_data
    stocks_data = fetch_stock_data()

    scheduler = BackgroundScheduler()
    scheduler.add_job(save_stock_data, 'interval', seconds=30)
    atexit.register(lambda: scheduler.shutdown())
    scheduler.start()

    for stock in stocks_data:
        refresh_interval = random.randint(1, 5)
        threading.Thread(target=refresh_stock_price, args=(stock['symbol'], refresh_interval)).start()

@app.route('/api/stock/<symbol>')
def get_stock_price(symbol):
    stock = next((s for s in stocks_data if s['symbol'] == symbol), None)
    if stock:
        return jsonify({'symbol': stock['symbol'], 'price': stock['price']})
    else:
        return jsonify({'error': 'Stock not found'}), 404

if __name__ == '__main__':
    initialize_stocks()
    app.run(debug=True)
