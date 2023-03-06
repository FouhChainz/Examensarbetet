import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("/data/data_totaled.csv")
# Replace any string values in the 'sold' column with NaN values

# Convert the 'sold' column to a numeric type
# Replace the "−" sign with "-"
df['temp'] = df['temp'].str.replace('−', '-')

# Convert the "temperature" column to numerical values
df['temp'] = pd.to_numeric(df['temp'], errors='coerce')


# Make sure the index column is in a datetime format
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Drop any rows with NaN values
df = df.dropna()
# Split the data into training and testing sets
X = df[['temp'
    , 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'weekday_7'
    , 'weather_status_Klart', 'weather_status_Moln', 'weather_status_Regn', 'weather_status_Snö']]
y = df[['sold']]

# Extract the features and target columns
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=120, shuffle=False)

model = LinearRegression()
# Fit a multiple linear regression model on the training data
reg = LinearRegression().fit(X_train, y_train)

# Use the model to make predictions on the test data
predictions = reg.predict(X_test)

# Calculate the mean squared error and root mean squared error
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)

# Print the MSE and RMSE
print('MSE:', mse)
print('RMSE:', rmse)

multiple_linear_regression_data = pd.DataFrame(predictions)
multiple_linear_regression_data.to_csv("multiple_linear_regression_data.csv",index=False)

# Plot the predicted sales vs actual sales
plt.plot(y.index,df['sold'], label="Sålda")
plt.plot(y_test.index,predictions, label="Prediktion")
plt.xlabel("Datum")
plt.ylabel("Antal sålda rätter")
plt.title("Sålda vs Förutspådd Försäljning")
plt.legend()
plt.show()

