import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            return None, "No data found for this ticker symbol"
        
        # Get company info
        info = stock.info
        company_name = info.get('longName', ticker)
        
        return data, company_name
    except Exception as e:
        return None, f"Error fetching data: {str(e)}"

def calculate_technical_indicators(data):
    """
    Calculate technical indicators
    """
    df = data.copy()
    
    # Moving Averages
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_21'] = df['Close'].rolling(window=21).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    
    # Volatility (Standard Deviation)
    df['Volatility'] = df['Close'].pct_change().rolling(window=21).std()
    
    return df

def calculate_risk_level(volatility):
    """
    Calculate risk level based on volatility
    """
    avg_volatility = volatility * 100  # Convert to percentage
    
    if avg_volatility < 1:
        return "Low", "#10b981"
    elif avg_volatility < 2:
        return "Medium", "#f59e0b"
    else:
        return "High", "#ef4444"

def generate_recommendation(current_price, predicted_prices):
    """
    Generate investment recommendation based on predicted trend
    """
    avg_predicted = np.mean(predicted_prices)
    price_change_pct = ((avg_predicted - current_price) / current_price) * 100
    
    if price_change_pct > 3:
        return "BUY", "#10b981", "Predicted upward trend detected"
    elif price_change_pct < -3:
        return "SELL", "#ef4444", "Predicted downward trend detected"
    else:
        return "HOLD", "#f59e0b", "No significant trend detected"

def prepare_chart_data(data, predictions):
    """
    Prepare data for charts
    """
    # Historical data
    historical = {
        'dates': data.index.strftime('%Y-%m-%d').tolist(),
        'close': data['Close'].tolist(),
        'ma7': data['MA_7'].fillna(0).tolist(),
        'ma21': data['MA_21'].fillna(0).tolist(),
        'ma50': data['MA_50'].fillna(0).tolist(),
    }
    
    # Prediction data
    last_date = data.index[-1]
    future_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                    for i in range(len(predictions))]
    
    prediction_data = {
        'dates': future_dates,
        'predictions': predictions.tolist()
    }
    
    # Combined for actual vs predicted chart
    combined_dates = historical['dates'][-30:] + future_dates
    combined_actual = historical['close'][-30:] + [None] * len(predictions)
    combined_predicted = [None] * 30 + predictions.tolist()
    
    combined = {
        'dates': combined_dates,
        'actual': combined_actual,
        'predicted': combined_predicted
    }
    
    return {
        'historical': historical,
        'predictions': prediction_data,
        'combined': combined
    }

def get_cached_data(ticker):
    """
    Get cached stock data if available
    """
    cache_file = f'data/{ticker}_cache.json'
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            # Cache valid for 1 hour
            if datetime.now() - cache_time < timedelta(hours=1):
                return cache['data']
    
    return None

def save_cache(ticker, data):
    """
    Save stock data to cache
    """
    os.makedirs('data', exist_ok=True)
    cache_file = f'data/{ticker}_cache.json'
    
    cache = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def validate_ticker(ticker):
    """
    Validate if ticker symbol exists
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return 'regularMarketPrice' in info or 'currentPrice' in info
    except:
        return False
