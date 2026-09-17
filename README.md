# AI Stock Forecasting & Investment Decision Support System

An AI-powered stock forecasting and investment decision support system built with Python, Machine Learning, Deep Learning, and Flask.

The application analyzes historical stock market data, predicts future stock prices using multiple forecasting models, visualizes actual vs. predicted prices, and provides BUY / SELL / HOLD decision-support signals based on price trends and volatility.

> **Disclaimer:** This project is developed for educational and research purposes. The predictions and signals should not be considered financial advice or a recommendation to buy or sell securities.

---

## 🚀 Project Overview

Stock market data contains complex patterns influenced by trends, volatility, and historical price movements. This project uses Machine Learning and Deep Learning techniques to analyze historical stock data and generate price forecasts.

The system provides:

- Historical stock data analysis
- Stock price forecasting
- Multiple Machine Learning models
- Deep Learning-based LSTM forecasting
- Actual vs. predicted price visualization
- Moving average analysis
- BUY / SELL / HOLD decision-support signals
- Trend and volatility analysis
- Interactive web interface using Flask

---

## ✨ Features

### 📊 Stock Data Analysis
- Fetches historical stock market data using Yahoo Finance
- Processes and cleans historical price data
- Calculates technical indicators such as Moving Average

### 🤖 Machine Learning Models

The project implements and compares:

- Linear Regression
- Random Forest Regressor
- LSTM (Long Short-Term Memory)

The models are evaluated using **Root Mean Squared Error (RMSE)**.

### 🧠 LSTM Forecasting

LSTM is used to capture sequential patterns in historical stock prices and generate future price predictions.

### 📈 Visualization

The application provides visualizations including:

- Historical stock prices
- Actual vs. predicted prices
- Moving Average (MA7)
- Forecast trends
- Price volatility

### 💡 Investment Decision Support

Based on the predicted trend and volatility, the system generates:

- **BUY**
- **SELL**
- **HOLD**

These signals are intended only as decision-support outputs for educational purposes.

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Flask Web Application
  │
  ├── Stock Symbol Input
  │
  ▼
Yahoo Finance
  │
  ▼
Historical Stock Data
  │
  ▼
Data Preprocessing
  │
  ├── Feature Preparation
  ├── Moving Average
  └── Volatility Analysis
  │
  ▼
Machine Learning Models
  │
  ├── Linear Regression
  ├── Random Forest
  └── LSTM
  │
  ▼
Model Evaluation
  │
  └── RMSE
  │
  ▼
Prediction & Trend Analysis
  │
  ▼
BUY / SELL / HOLD
  │
  ▼
Web Dashboard

🛠️ Technologies Used
Programming Language
Python
Machine Learning & Data Science
NumPy
Pandas
Scikit-learn
TensorFlow
Keras
Web Development
Flask
HTML5
CSS3
JavaScript
Chart.js
Data Source
Yahoo Finance
yfinance
Visualization
Matplotlib
Chart.js
Development Tools
Git
GitHub
VS Code

stock_forecasting/
│
├── model/
│   ├── __init__.py
│   ├── predict.py
│   └── train_model.py
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── data/
│
├── app.py
├── requirements.txt
├── .gitignore
├── run.bat
├── run.sh
├── check_system.py
├── PROJECT_STRUCTURE.txt
├── QUICK_REFERENCE.txt
├── SETUP_GUIDE.txt
├── START_HERE.txt
└── README.md

⚙️ Installation
1. Clone the Repository
git clone https://github.com/sanjaiXD/ai-stock-forecasting-investment-support.git
2. Navigate to the Project
cd ai-stock-forecasting-investment-support
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment
Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
▶️ Running the Application
Windows
python app.py

or use:

run.bat
macOS / Linux
python app.py

or:

./run.sh

After starting the Flask server, open the local URL displayed in the terminal.

📊 Model Evaluation

The system compares different forecasting approaches using Root Mean Squared Error (RMSE).

RMSE

RMSE measures the difference between actual stock prices and predicted stock prices.

RMSE = √(Mean((Actual - Predicted)²))

A lower RMSE indicates that the model's predictions are closer to the actual values on the evaluated dataset.

🔄 Workflow
User enters a stock symbol.
Historical stock data is retrieved.
Data is cleaned and prepared.
Relevant features are generated.
Multiple forecasting models are trained.
Models generate price predictions.
Models are evaluated using RMSE.
Actual and predicted prices are visualized.
Trend and volatility are analyzed.
A BUY / SELL / HOLD decision-support signal is generated.
🎯 Key Learning Outcomes

This project demonstrates practical experience with:

Python programming
Data preprocessing
Exploratory data analysis
Machine Learning
Deep Learning
Time-series forecasting
LSTM networks
Model evaluation
REST/web application development
Flask
Data visualization
Git and GitHub
Integrating financial data APIs
🔮 Future Enhancements

Potential improvements include:

Real-time stock market data integration
Additional technical indicators such as RSI and MACD
Advanced time-series models
Transformer-based forecasting
Portfolio-level analysis
News sentiment analysis
Financial news and social-media sentiment integration
Improved risk analysis
Cloud deployment
Automated model retraining
👨‍💻 Author

Sanjai R

MCA Graduate | Python | Machine Learning | AI | Flask

GitHub:
https://github.com/sanjaiXD

Portfolio:
https://sanjaixd.github.io/sanjai-ravi.github.io/

LinkedIn:
https://linkedin.com/in/sanjai-ravi-8892b8374

📜 License

This project is intended for educational and research purposes.


### One important thing

Because your GitHub repository currently has the project structure being organized, put this `README.md` **in the main/root folder**, at the same level as:

```text
app.py
requirements.txt
model/
static/
templates/
README.md

Then run:

git add README.md
git commit -m "Add professional project README"
git push

Once pushed, GitHub will automatically display the README on the repository's main page.
