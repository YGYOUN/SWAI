from flask import Flask, request, jsonify
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime

app = Flask(__name__)

# 1. Yahoo Finance 데이터 가져오기
def fetch_yahoo_data(symbol="NQ=F", interval="1h", period="1mo"):
    data = yf.download(symbol, interval=interval, period=period)
    data['DateTime'] = data.index
    data.reset_index(drop=True, inplace=True)
    return data

# 2. 보조지표 계산 함수
def calculate_indicators(data):
    data['ATR'] = (data['High'] - data['Low']).rolling(window=14).mean()
    data['Momentum'] = data['Close'] - data['Close'].shift(10)
    data['ROC'] = ((data['Close'] - data['Close'].shift(10)) / data['Close'].shift(10)) * 100
    data['Williams %R'] = ((data['High'].rolling(window=14).max() - data['Close']) / (data['High'].rolling(window=14).max() - data['Low'].rolling(window=14).min())) * -100
    data['Stochastic %K'] = ((data['Close'] - data['Low'].rolling(window=14).min()) / (data['High'].rolling(window=14).max() - data['Low'].rolling(window=14).min())) * 100
    data['Stochastic %D'] = data['Stochastic %K'].rolling(window=3).mean()
    return data

# 3. CSV 데이터와 결합
def merge_data_with_indicators(csv_data, indicators):
    trades = pd.DataFrame(csv_data)
    trades['DateTime'] = pd.to_datetime(trades['날짜/시간'])
    indicators['DateTime'] = pd.to_datetime(indicators['DateTime'])
    merged = pd.merge_asof(trades.sort_values('DateTime'), indicators.sort_values('DateTime'), on='DateTime')
    return merged

# 4. 엔드포인트 정의
@app.route('/process-csv', methods=['POST'])
def process_csv():
    try:
        # 클라이언트에서 받은 CSV 데이터
        data = request.get_json()
        csv_data = pd.read_csv(pd.compat.StringIO(data['csv']))

        # Yahoo Finance에서 데이터 다운로드 및 보조지표 계산
        symbol = "NQ=F"  # 나스닥 100 선물 심볼
        market_data = fetch_yahoo_data(symbol)
        indicators = calculate_indicators(market_data)

        # CSV와 보조지표 병합
        result = merge_data_with_indicators(csv_data, indicators)

        # JSON으로 반환
        return jsonify(result.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
