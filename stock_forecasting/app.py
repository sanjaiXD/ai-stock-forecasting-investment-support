from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys
import os

# Add model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from model.train_model import StockPredictor
from model.predict import (
    fetch_stock_data, 
    calculate_technical_indicators,
    calculate_risk_level,
    generate_recommendation,
    prepare_chart_data,
    validate_ticker
)

app = Flask(__name__)
CORS(app)

# Global variable to store last prediction results
last_prediction = {}

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/validate_ticker', methods=['POST'])
def validate_ticker_route():
    """Validate ticker symbol"""
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    
    if not ticker:
        return jsonify({'valid': False, 'message': 'Please enter a ticker symbol'})
    
    is_valid = validate_ticker(ticker)
    
    if is_valid:
        return jsonify({'valid': True, 'message': 'Valid ticker symbol'})
    else:
        return jsonify({'valid': False, 'message': 'Invalid ticker symbol or no data available'})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Validate inputs
        if not ticker:
            return jsonify({'error': 'Please provide a ticker symbol'}), 400
        
        if not start_date or not end_date:
            # Default to last 2 years
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        
        # Fetch stock data
        stock_data, result = fetch_stock_data(ticker, start_date, end_date)
        
        if stock_data is None:
            return jsonify({'error': result}), 400
        
        company_name = result
        
        # Check if enough data
        if len(stock_data) < 100:
            return jsonify({'error': 'Not enough historical data. Please select a longer date range.'}), 400
        
        # Calculate technical indicators
        stock_data = calculate_technical_indicators(stock_data)
        
        # Train models
        predictor = StockPredictor(stock_data)
        model_comparison = predictor.train_all_models()
        
        # Predict next 7 days
        predictions = predictor.predict_future(days=7)
        
        # Get current price
        current_price = float(stock_data['Close'].iloc[-1])
        
        # Calculate volatility for risk assessment
        volatility = stock_data['Volatility'].iloc[-1]
        risk_level, risk_color = calculate_risk_level(volatility)
        
        # Generate recommendation
        recommendation, rec_color, rec_reason = generate_recommendation(current_price, predictions)
        
        # Prepare chart data
        chart_data = prepare_chart_data(stock_data, predictions)
        
        # Get last updated time
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare response
        response = {
            'success': True,
            'ticker': ticker,
            'company_name': company_name,
            'current_price': round(current_price, 2),
            'predicted_price': round(float(predictions[-1]), 2),
            'avg_predicted_price': round(float(np.mean(predictions)), 2),
            'price_change': round(float(predictions[-1] - current_price), 2),
            'price_change_percent': round(((predictions[-1] - current_price) / current_price) * 100, 2),
            'recommendation': recommendation,
            'recommendation_color': rec_color,
            'recommendation_reason': rec_reason,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'volatility': round(volatility * 100, 2),
            'predictions': predictions.tolist(),
            'model_comparison': model_comparison,
            'chart_data': chart_data,
            'last_updated': last_updated,
            'data_points': len(stock_data)
        }
        
        # Store for later retrieval
        global last_prediction
        last_prediction = response
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/data', methods=['GET'])
def get_historical_data():
    """Get historical stock data"""
    ticker = request.args.get('ticker', '').upper()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not ticker:
        return jsonify({'error': 'Please provide a ticker symbol'}), 400
    
    # Fetch data
    stock_data, result = fetch_stock_data(ticker, start_date, end_date)
    
    if stock_data is None:
        return jsonify({'error': result}), 400
    
    # Calculate technical indicators
    stock_data = calculate_technical_indicators(stock_data)
    
    # Prepare response
    response = {
        'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
        'close': stock_data['Close'].tolist(),
        'open': stock_data['Open'].tolist(),
        'high': stock_data['High'].tolist(),
        'low': stock_data['Low'].tolist(),
        'volume': stock_data['Volume'].tolist(),
        'ma7': stock_data['MA_7'].fillna(0).tolist(),
        'ma21': stock_data['MA_21'].fillna(0).tolist(),
        'ma50': stock_data['MA_50'].fillna(0).tolist(),
    }
    
    return jsonify(response)

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Get forecast data"""
    if not last_prediction:
        return jsonify({'error': 'No prediction available. Please run prediction first.'}), 400
    
    return jsonify({
        'predictions': last_prediction.get('predictions', []),
        'chart_data': last_prediction.get('chart_data', {})
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("=" * 60)
    print("🚀 AI-Driven Stock Forecasting System")
    print("=" * 60)
    print("Starting Flask server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
