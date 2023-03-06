import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load data
weather = pd.read_csv("/Users/christianzhaco/Skola/PycharmProjects/Examensarbete/data/weather_main.csv")
sales = pd.read_csv("/Users/christianzhaco/Skola/PycharmProjects/Examensarbete/data/dishes_main.csv")

# Merge data into a single dataframe
df = pd.merge(weather, sales, on='date')
df[ 'date' ]=pd.to_datetime(df[ 'date' ])
df=df.set_index('date')

# Extract predictor and response variables
X = df[['temp']]
y = df[['sold']]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=110, shuffle=False)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("Mean Squared Error: ", mse)
print("Root Mean Squared Error: ", rmse)
print(y_pred)


#Function to save results as a csv file
comparison = pd.DataFrame(y_pred)
comparison.to_csv("comparison.csv",index=False)

# Plot actual vs predicted sales
plt.plot(y.index,y, label="Sålda")
plt.plot(y_test.index,y_pred, label="Prediktion")
plt.xlabel("Datum")
plt.ylabel("Antal sålda rätter")
plt.title("Sålda vs Förutspådd Försäljning")
plt.legend()
plt.show()
