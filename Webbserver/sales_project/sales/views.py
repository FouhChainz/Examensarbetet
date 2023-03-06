import datetime
import pandas as pd
import numpy as np
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import SalesUploadForm
from .models import *
from .ml_models import train_multiple_linear_regression_model
import json


def home (request):
    return render(request, "base.html")


def predict_sales (request):
    if request.method == 'POST':
        form=SalesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Load the CSV file into a Pandas DataFrame
            csv_file=request.FILES[ 'file' ]
            df=pd.read_csv(csv_file)
            # Convert the "temperature" column to numerical values
            df[ 'temp' ]=df[ 'temp' ].str.replace('−', '-')
            df[ 'temp' ]=pd.to_numeric(df[ 'temp' ], errors='coerce')
            # df[ 'date' ]=df[ 'date' ].astype(str)

            # Make sure the index column is in a datetime format
            # df[ 'date' ]=pd.to_datetime(df[ 'date' ])
            # df=df.set_index('date')
            df=df.dropna()

            # Train the multiple linear regression model
            model=train_multiple_linear_regression_model(df)

            # Define the feature columns for prediction
            feature_cols=[ 'temp', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6',
                           'weekday_7', 'weather_status_Klart', 'weather_status_Moln', 'weather_status_Regn',
                           'weather_status_Snö' ]

            # Create a DataFrame containing only the features for the last 120 days
            X_pred=df.iloc[ -120:, : ].loc[ :, feature_cols ]

            # Use the trained model to predict the sales for the last three months
            y_pred=model.predict(X_pred)

            # Add the predicted sales as a new column to the DataFrame
            df_pred=X_pred.copy()
            df_pred[ 'sold' ]=y_pred
            df_pred.insert(0, 'date', df[ 'date' ], False)

            # Save the predicted sales to the database
            for index, row in df_pred.iterrows():
                Sales.objects.create(date=row[ 'date' ],
                                     sold=row[ 'sold' ],
                                     temp=row[ 'temp' ],
                                     weekday_1=row[ 'weekday_1' ],
                                     weekday_2=row[ 'weekday_2' ],
                                     weekday_3=row[ 'weekday_3' ],
                                     weekday_4=row[ 'weekday_4' ],
                                     weekday_5=row[ 'weekday_5' ],
                                     weekday_6=row[ 'weekday_6' ],
                                     weekday_7=row[ 'weekday_7' ],
                                     weather_status_Klart=row[ 'weather_status_Klart' ],
                                     weather_status_Moln=row[ 'weather_status_Moln' ],
                                     weather_status_Regn=row[ 'weather_status_Regn' ],
                                     weather_status_Sno=row[ 'weather_status_Snö' ]
                                     )

            # Render the predicted sales in a chart
            chart_data=Sales.objects.all()
            return render(request, 'predict_sales.html', {'chart_data':chart_data})
        else:
            print(form.errors)
    else:
        form=SalesUploadForm()
        return render(request, 'upload_sales.html', {'form':form})
    return HttpResponse("Error: form is invalid")


def sales_chart (request):
    actual_sold_stuff=Actual_Sold.objects.all().order_by('date')
    predicts=Sales.objects.all().order_by('date')
    labels=[ ]
    data=[ ]
    data2=[ ]
    i = 0
    while i < 240:
        data.append("NaN")
        i +=1
    for sale in predicts:
        data.append(sale.sold)
    for sale in actual_sold_stuff:
        labels.append(datetime.datetime.strptime(sale.date, '%Y-%m-%d').strftime('%Y-%m-%d'))
        data2.append(sale.sold)

    actual_sales_data=Actual_Sold.objects.all().order_by('date')
    predicted_sales_data=Sales.objects.all().order_by('date')

    actual_sales={}
    predicted_sales={}

    for sale in actual_sales_data:
        actual_sales[ sale.date ]=sale.sold


    for sale in predicted_sales_data:
        predicted_sales[ sale.date ]=sale.sold

    table_data=[ ]
    for date, actual in actual_sales.items():
        if date in predicted_sales:
            predicted=predicted_sales[ date ]
            difference=predicted - actual
            table_data.append({'date':date, 'actual_sold':actual, 'predicted_sold':predicted, 'difference':difference})

    context = {
        'labels':labels,
        'values':data2,
        'data':data,
        'actual_sales':actual_sales,
        'predicted_sales':predicted_sales,
        'table_data':table_data,
    }

    return render(request, 'sales_chart.html', context=context)


