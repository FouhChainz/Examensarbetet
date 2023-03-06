from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load the data
df = pd.read_csv("/data/data_totaled.csv")

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

# Split the data into training and testing sets
train_data, test_data, train_target, test_target= train_test_split(X, y, test_size=110, shuffle=False)

# Create the Random Forest Regression model
rf_model = RandomForestRegressor()

# Train the model
rf_model.fit(train_data, train_target.values.ravel())

# Make predictions on the test data
predictions = rf_model.predict(test_data)

# Evaluate the model
score = rf_model.score(test_data, test_target)
print("Model score: {:.2f}%".format(score * 100))

# Calculate the mean squared error and root mean squared error
mse = mean_squared_error(test_target, predictions)
rmse = np.sqrt(mse)

# Print the MSE and RMSE
print('MSE:', mse)
print('RMSE:', rmse)


# Plot the predicted sales vs actual sales
plt.plot(y.index,df['sold'], label="Sålda")
plt.plot(test_target.index,predictions, label="Prediktion")
plt.xlabel("Datum")
plt.ylabel("Antalet sålda rätter")
plt.title("Aktuell vs Förutspådd Försäljning")
plt.legend()
plt.show()
