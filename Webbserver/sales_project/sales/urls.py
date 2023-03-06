from django.urls import path, include
from .views import *

app_name = 'sales'

urlpatterns = [
    path('', home, name='home'),
    path('predict_sales/', predict_sales, name='predict_sales'),
    path('sales_chart/', sales_chart, name='sales_chart3'),

]
