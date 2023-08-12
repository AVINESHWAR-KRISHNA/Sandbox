import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.legacy import Adam as LegacyAdam
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

# Step 1: Data Collection
def fetch_historical_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Example usage:
symbol = "TCS.NS"  # Replace with the desired stock symbol
start_date = "2020-01-01"
end_date = "2023-07-22"
historical_data = fetch_historical_data(symbol, start_date, end_date)

# Step 2: Data Preprocessing
def preprocess_data(data):
    # Use 'Close' prices for prediction
    data = data[['Close']]

    # Drop any rows with missing values (if any)
    data = data.dropna()

    # Normalize the 'Close' prices using Min-Max scaling
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    return data_scaled, scaler

data_scaled, scaler = preprocess_data(historical_data)

# Step 3: Splitting Data (Training and Testing Sets)
def train_test_split(data_scaled, train_size=0.8):
    split_index = int(len(data_scaled) * train_size)
    train_data, test_data = data_scaled[:split_index], data_scaled[split_index:]
    return train_data, test_data

train_data, test_data = train_test_split(data_scaled)

# Step 4: Model Selection and Training (LSTM)
def train_lstm_model(train_data, look_back=60, epochs=500, batch_size=64, validation_split=0.2):
    X_train, y_train = [], []
    for i in range(len(train_data) - look_back):
        X_train.append(train_data[i : i + look_back])
        y_train.append(train_data[i + look_back])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshape the data for LSTM input: (samples, time steps, features)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Build the LSTM model
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(look_back, 1)),
        Dropout(0.2),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(64),
        BatchNormalization(),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])

    # Compile the model with the LegacyAdam optimizer and learning rate scheduler
    def lr_schedule(epoch):
        lr = 0.001
        if epoch > 100:
            lr *= 0.1
        elif epoch > 50:
            lr *= 0.5
        return lr

    model.compile(optimizer=LegacyAdam(learning_rate=lr_schedule(0)), loss='mean_squared_error')

    # Early stopping to prevent overfitting
    early_stopping = EarlyStopping(patience=50, restore_best_weights=True)

    # Train the LSTM model with validation split
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1,
              callbacks=[early_stopping, LearningRateScheduler(lr_schedule)], validation_split=validation_split)

    return model

# Example usage:
look_back = 60
validation_split = 0.2  # 20% of the training data will be used for validation
lstm_model = train_lstm_model(train_data, look_back=look_back, validation_split=validation_split)

# Step 5: Evaluating the LSTM Model
def evaluate_lstm_model(model, test_data, look_back, scaler):
    X_test, y_test = [], []
    for i in range(len(test_data) - look_back):
        X_test.append(test_data[i : i + look_back])
        y_test.append(test_data[i + look_back])
    X_test, y_test = np.array(X_test), np.array(y_test)

    # Reshape the data for LSTM input: (samples, time steps, features)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Make predictions using the LSTM model
    y_pred = model.predict(X_test)

    # Inverse transform the predictions and actual values to the original scale
    y_pred = scaler.inverse_transform(y_pred)
    y_test = scaler.inverse_transform(y_test)

    # Calculate Mean Absolute Error (MAE)
    mae = np.mean(np.abs(y_pred - y_test))

    return mae, y_pred

# Example usage:
mae_lstm, predictions = evaluate_lstm_model(lstm_model, test_data, look_back, scaler)
print(f"LSTM Mean Absolute Error (MAE): {mae_lstm}")

# Step 6: Visualizations (Plotting Actual and Predicted Prices)
def plot_predictions(actual, predicted):
    time_steps = np.arange(len(actual))

    plt.figure(figsize=(12, 6))
    plt.plot(time_steps, actual, label='Actual Prices', color='blue')
    plt.plot(time_steps, predicted, label='Predicted Prices', color='red')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.title('Actual vs. Predicted Stock Prices')
    plt.legend()
    plt.xticks(time_steps, rotation=45)
    plt.show()

# Visualization of Actual and Predicted Prices
actual_prices = scaler.inverse_transform(test_data[look_back:])
predicted_prices = predictions
plot_predictions(actual_prices, predicted_prices)

# Combine the actual and predicted data along with all columns from yfinance data into a tabular format
def create_tabular_data_with_all_columns(yfinance_data, actual_prices, predicted_prices, scaler):
    # Inverse transform the original data to the original scale
    actual_prices = scaler.inverse_transform(actual_prices)

    # Create a DataFrame with the original data and predicted prices
    data = yfinance_data.iloc[-len(actual_prices):].copy()  # Get the relevant rows from yfinance data

    # Add the date, actual, and predicted prices as new columns
    data['Date'] = data.index
    data['Actual Prices'] = actual_prices.flatten()
    data['Predicted Prices'] = predicted_prices.flatten()

    return data

# Create the tabular data with all columns
tabular_data_with_all_columns = create_tabular_data_with_all_columns(historical_data, actual_prices, predicted_prices, scaler)

reordered_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Actual Prices', 'Predicted Prices']
tabular_data_with_all_columns = tabular_data_with_all_columns[reordered_columns]

# Display the tabular data
print(tabular_data_with_all_columns.to_string(index=False))
