from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def train_multiple_linear_regression_model (df):
    # Split the data into features and target
    X=df[ ['temp'
        , 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'weekday_7'
        , 'weather_status_Klart', 'weather_status_Moln', 'weather_status_Regn', 'weather_status_Snö' ] ]
    y=df[ [ 'sold' ] ]

    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=120, shuffle=False)

    # Train the model on the feature and target data
    model = LinearRegression()
    reg = LinearRegression().fit(X_train, y_train)

    return reg
