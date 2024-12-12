from flask import Flask, request, jsonify
import pandas as pd
import requests
import time
from io import StringIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 허용

API_KEY = 'SYSK8VGIVQQNK0KZ'  # Replace with your actual API key
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_indicators(symbol, datetime):
    indicators = []
    functions = [
        'SMA', 'EMA', 'WMA', 'DEMA', 'RSI', 'ADX', 'AROON', 'CCI',
        'BBANDS', 'MFI', 'STOCH', 'TEMA', 'TRIX', 'WILLR', 'ROC', 'ATR',
        'OBV', 'ADOSC', 'SAR', 'KAMA'
    ]
    for function in functions:
        try:
            response = requests.get(BASE_URL, params={
                'function': function,
                'symbol': symbol,
                'apikey': API_KEY,
                'interval': '1min',
                'time_period': 14,
                'series_type': 'close'
            })
            data = response.json()
            indicators.append(data.get('Technical Analysis: ' + function, {}).get(datetime, None))
            time.sleep(12)  # To respect API limits
        except Exception as e:
            indicators.append(None)
    return indicators


@app.route('/process-csv', methods=['POST'])
def process_csv():
    try:
        data = request.json.get('csv', None)
        if not data:
            return jsonify({'error': 'CSV 데이터가 제공되지 않았습니다.'}), 400

        csv_data = pd.read_csv(StringIO(data))
        csv_data['Indicators'] = csv_data.apply(
            lambda row: fetch_indicators('NQF', row['날짜/시간']), axis=1
        )
        grouped_data = {
            'entryLong': csv_data[csv_data['타입'] == '엔트리 롱'].to_dict(orient='records'),
            'entryShort': csv_data[csv_data['타입'] == '엔트리 숏'].to_dict(orient='records'),
            'exitLong': csv_data[csv_data['타입'] == '엑시트 롱'].to_dict(orient='records'),
            'exitShort': csv_data[csv_data['타입'] == '엑시트 숏'].to_dict(orient='records'),
        }
        return jsonify(grouped_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
