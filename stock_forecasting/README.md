# 🚀 AI-Driven Stock Forecasting and Investment Decision Support System

A complete full-stack web application that uses Machine Learning and Deep Learning to predict stock prices and provide investment recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Screenshots](#screenshots)
- [Disclaimer](#disclaimer)

## ✨ Features

### 🤖 Machine Learning Models
- **Linear Regression**: Fast baseline model for trend analysis
- **Random Forest Regressor**: Ensemble learning for robust predictions
- **LSTM Neural Network**: Deep learning for complex time-series patterns
- **Automatic Model Selection**: System selects the best performing model based on RMSE

### 📊 Data Analysis
- Real-time stock data fetching via Yahoo Finance API
- Historical price visualization with interactive charts
- Technical indicators: Moving Averages (MA7, MA21, MA50)
- Volatility analysis and risk assessment

### 💡 Investment Insights
- **BUY/SELL/HOLD Recommendations**: Based on predicted trends
- **Risk Level Assessment**: Low/Medium/High based on volatility
- **7-Day Price Forecasting**: Predict future stock prices
- **Model Performance Comparison**: View RMSE and MAE metrics

### 🎨 User Interface
- Modern dark-themed finance dashboard
- Responsive design for all devices
- Interactive charts using Chart.js
- Real-time data updates
- Loading animations and error handling

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **NumPy & Pandas** - Data processing
- **Scikit-Learn** - Traditional ML models
- **TensorFlow/Keras** - Deep learning (LSTM)
- **yfinance** - Stock data API

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **Fetch API** - Asynchronous requests

## 📁 Project Structure

```
stock_forecasting/
│
├── app.py                      # Flask application (main entry point)
├── requirements.txt            # Python dependencies
│
├── model/                      # Machine Learning models
│   ├── __init__.py
│   ├── train_model.py         # Model training logic (LR, RF, LSTM)
│   └── predict.py             # Prediction utilities
│
├── static/                     # Frontend assets
│   ├── style.css              # Styling (dark theme)
│   └── script.js              # JavaScript logic
│
├── templates/                  # HTML templates
│   └── index.html             # Main dashboard page
│
├── data/                       # Data storage (auto-created)
│   └── cache/                 # Cached stock data
│
└── README.md                   # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (for TensorFlow)

### Step 1: Clone or Extract the Project

```bash
cd stock_forecasting
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- NumPy 1.24.3
- Pandas 2.0.3
- Matplotlib 3.7.2
- Seaborn 0.12.2
- Scikit-Learn 1.3.0
- TensorFlow 2.15.0
- yfinance 0.2.28
- Flask-CORS 4.0.0

**Note**: TensorFlow installation may take a few minutes.

### Step 4: Run the Application

```bash
python app.py
```

You should see:
```
============================================================
🚀 AI-Driven Stock Forecasting System
============================================================
Starting Flask server...
Access the application at: http://127.0.0.1:5000
============================================================
```

### Step 5: Open in Browser

Navigate to: **http://127.0.0.1:5000**

## 🎯 Usage

### Basic Workflow

1. **Enter Stock Symbol**: Type a ticker symbol (e.g., AAPL, TSLA, GOOGL, MSFT)
   - US Stocks: AAPL, TSLA, GOOGL, MSFT, AMZN
   - Indian Stocks: INFY.NS, TCS.NS, RELIANCE.NS

2. **Select Date Range**: Choose start and end dates (minimum 100 days recommended)
   - Default: Last 2 years
   - More data = Better predictions

3. **Click "Predict Stock Price"**: The system will:
   - Fetch historical data from Yahoo Finance
   - Train 3 ML models (Linear Regression, Random Forest, LSTM)
   - Select the best model automatically
   - Generate predictions for next 7 days

4. **View Results**:
   - Current price and predicted price
   - BUY/SELL/HOLD recommendation
   - Risk assessment (Low/Medium/High)
   - Interactive charts
   - Model performance comparison

### Example Tickers

| Symbol | Company | Market |
|--------|---------|--------|
| AAPL | Apple Inc. | NASDAQ |
| TSLA | Tesla Inc. | NASDAQ |
| GOOGL | Alphabet Inc. | NASDAQ |
| MSFT | Microsoft Corp. | NASDAQ |
| AMZN | Amazon.com Inc. | NASDAQ |
| INFY.NS | Infosys Limited | NSE India |
| TCS.NS | Tata Consultancy | NSE India |

## 🌐 API Endpoints

### POST /api/predict
Predict stock prices and generate recommendations.

**Request:**
```json
{
  "ticker": "AAPL",
  "start_date": "2022-01-01",
  "end_date": "2024-01-01"
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "current_price": 185.50,
  "predicted_price": 192.30,
  "recommendation": "BUY",
  "risk_level": "Low",
  "predictions": [186.2, 187.5, 189.1, 190.4, 191.2, 191.8, 192.3],
  "model_comparison": {...},
  "chart_data": {...}
}
```

### GET /api/data
Fetch historical stock data with technical indicators.

**Parameters:**
- `ticker`: Stock symbol
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

### GET /api/forecast
Get the last prediction results.

### GET /health
Health check endpoint.

## 🧠 Models

### 1. Linear Regression
- **Type**: Traditional ML
- **Use Case**: Baseline predictions
- **Speed**: Very Fast
- **Accuracy**: Moderate

### 2. Random Forest Regressor
- **Type**: Ensemble Learning
- **Use Case**: Robust predictions
- **Speed**: Fast
- **Accuracy**: Good

### 3. LSTM (Long Short-Term Memory)
- **Type**: Deep Learning
- **Use Case**: Complex patterns
- **Speed**: Slower
- **Accuracy**: Best for time series

**Model Selection**: The system automatically selects the model with the lowest RMSE (Root Mean Squared Error).

## 📊 Technical Indicators

- **Moving Averages**: MA7, MA21, MA50
- **Volatility**: Standard deviation of returns
- **Price Trends**: Upward/Downward momentum
- **Volume Analysis**: Trading volume patterns

## 🎨 Features Showcase

### Recommendation Logic

```python
if predicted_change > 3%:
    return "BUY"
elif predicted_change < -3%:
    return "SELL"
else:
    return "HOLD"
```

### Risk Assessment

```python
if volatility < 1%:
    return "Low Risk"
elif volatility < 2%:
    return "Medium Risk"
else:
    return "High Risk"
```

## ⚠️ Disclaimer

**IMPORTANT**: This system is designed for **educational and analytical purposes only**.

- ❌ **NOT** financial advice
- ❌ **NOT** a guarantee of future performance
- ❌ **NOT** a substitute for professional consultation

**Stock market investments carry inherent risks:**
- Past performance does not guarantee future results
- Predictions are based on historical data and may not reflect actual future prices
- Always conduct your own research
- Consult with licensed financial advisors before making investment decisions

The creators of this system are not responsible for any financial losses incurred.

## 🐛 Troubleshooting

### Common Issues

**1. TensorFlow Installation Fails**
```bash
# Use CPU-only version
pip install tensorflow-cpu==2.15.0
```

**2. "No module named 'yfinance'"**
```bash
pip install yfinance --upgrade
```

**3. "Invalid ticker symbol"**
- Check if the symbol is correct (e.g., AAPL not Apple)
- For international stocks, use proper suffix (e.g., .NS for India)

**4. "Not enough historical data"**
- Select a longer date range (at least 100 trading days)
- Some stocks may have limited historical data

**5. Port 5000 already in use**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 🚀 Performance Tips

1. **First Run**: Model training takes 30-60 seconds
2. **Caching**: Subsequent runs are faster (data cached for 1 hour)
3. **Data Range**: Use 1-2 years for optimal performance
4. **Model Selection**: LSTM is most accurate but slower to train

## 📝 Future Enhancements

- [ ] User authentication and portfolio tracking
- [ ] Multiple stock comparison
- [ ] Sentiment analysis from news
- [ ] More technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Export reports to PDF
- [ ] Email alerts for price targets
- [ ] Support for cryptocurrency predictions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ using Flask, TensorFlow, and Scikit-Learn

---

**Happy Investing! 📈💰**

*Remember: Invest wisely, diversify your portfolio, and never invest more than you can afford to lose.*
