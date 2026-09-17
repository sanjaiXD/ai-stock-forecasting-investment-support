import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import warnings
warnings.filterwarnings('ignore')

class StockPredictor:
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.sequence_length = 60
        
    def prepare_data(self):
        """Prepare and preprocess data for training"""
        # Use Close price for prediction
        self.data = self.data[['Close']].copy()
        
        # Handle missing values
        self.data.ffill(inplace=True)
        self.data.bfill(inplace=True)
        
        # Normalize data
        scaled_data = self.scaler.fit_transform(self.data)
        
        return scaled_data
    
    def create_sequences(self, data, seq_length):
        """Create sequences for time series prediction"""
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)
    
    def train_linear_regression(self, X_train, y_train, X_test, y_test):
        """Train Linear Regression model"""
        # Reshape for sklearn
        X_train_lr = X_train.reshape(X_train.shape[0], -1)
        X_test_lr = X_test.reshape(X_test.shape[0], -1)
        
        lr_model = LinearRegression()
        lr_model.fit(X_train_lr, y_train)
        
        predictions = lr_model.predict(X_test_lr)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        
        self.models['Linear Regression'] = {
            'model': lr_model,
            'rmse': rmse,
            'mae': mae,
            'type': 'sklearn'
        }
        
        return rmse, mae
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model"""
        # Reshape for sklearn
        X_train_rf = X_train.reshape(X_train.shape[0], -1)
        X_test_rf = X_test.reshape(X_test.shape[0], -1)
        
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        rf_model.fit(X_train_rf, y_train)
        
        predictions = rf_model.predict(X_test_rf)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        
        self.models['Random Forest'] = {
            'model': rf_model,
            'rmse': rmse,
            'mae': mae,
            'type': 'sklearn'
        }
        
        return rmse, mae
    
    def train_lstm(self, X_train, y_train, X_test, y_test):
        """Train LSTM Neural Network"""
        # Reshape for LSTM [samples, time steps, features]
        X_train_lstm = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test_lstm = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        
        # Build LSTM model
        lstm_model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(X_train_lstm.shape[1], 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50),
            Dropout(0.2),
            Dense(units=1)
        ])
        
        lstm_model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Train with reduced epochs for faster processing
        lstm_model.fit(X_train_lstm, y_train, epochs=20, batch_size=32, verbose=0)
        
        predictions = lstm_model.predict(X_test_lstm, verbose=0)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        
        self.models['LSTM'] = {
            'model': lstm_model,
            'rmse': rmse,
            'mae': mae,
            'type': 'lstm'
        }
        
        return rmse, mae
    
    def train_all_models(self):
        """Train all models and select the best one"""
        # Prepare data
        scaled_data = self.prepare_data()
        
        # Create sequences
        X, y = self.create_sequences(scaled_data, self.sequence_length)
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train all models
        print("Training Linear Regression...")
        lr_rmse, lr_mae = self.train_linear_regression(X_train, y_train, X_test, y_test)
        
        print("Training Random Forest...")
        rf_rmse, rf_mae = self.train_random_forest(X_train, y_train, X_test, y_test)
        
        print("Training LSTM...")
        lstm_rmse, lstm_mae = self.train_lstm(X_train, y_train, X_test, y_test)
        
        # Select best model based on RMSE
        best_rmse = min(lr_rmse, rf_rmse, lstm_rmse)
        
        if best_rmse == lr_rmse:
            self.best_model_name = 'Linear Regression'
        elif best_rmse == rf_rmse:
            self.best_model_name = 'Random Forest'
        else:
            self.best_model_name = 'LSTM'
        
        self.best_model = self.models[self.best_model_name]
        
        return {
            'Linear Regression': {'RMSE': lr_rmse, 'MAE': lr_mae},
            'Random Forest': {'RMSE': rf_rmse, 'MAE': rf_mae},
            'LSTM': {'RMSE': lstm_rmse, 'MAE': lstm_mae},
            'Best Model': self.best_model_name
        }
    
    def predict_future(self, days=7):
        """Predict future stock prices"""
        # Get last sequence_length days
        last_sequence = self.data[-self.sequence_length:].values
        last_sequence_scaled = self.scaler.transform(last_sequence)
        
        predictions = []
        current_sequence = last_sequence_scaled.copy()
        
        for _ in range(days):
            if self.best_model['type'] == 'sklearn':
                # Reshape for sklearn models
                X_pred = current_sequence.reshape(1, -1)
                next_pred = self.best_model['model'].predict(X_pred)[0]
            else:  # LSTM
                # Reshape for LSTM
                X_pred = current_sequence.reshape(1, self.sequence_length, 1)
                next_pred = self.best_model['model'].predict(X_pred, verbose=0)[0][0]
            
            predictions.append(next_pred)
            
            # Update sequence
            current_sequence = np.append(current_sequence[1:], [[next_pred]], axis=0)
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions)
        
        return predictions.flatten()
    
    def get_model_comparison(self):
        """Get comparison of all models"""
        comparison = {}
        for name, model_data in self.models.items():
            comparison[name] = {
                'RMSE': round(model_data['rmse'], 4),
                'MAE': round(model_data['mae'], 4)
            }
        return comparison
