from django.contrib import admin
from django.urls import path, include
from sales import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sales.urls')),
    path('predict_sales/',views.predict_sales,name="predict_sales"),
    path('sales_chart/', views.sales_chart, name='sales_chart3'),

]
