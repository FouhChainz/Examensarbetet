from django.db import models


class Sales(models.Model):
    date=models.CharField(max_length=10, primary_key=True)
    sold=models.IntegerField()
    temp=models.FloatField()
    weekday_1=models.BooleanField()
    weekday_2=models.BooleanField()
    weekday_3=models.BooleanField()
    weekday_4=models.BooleanField()
    weekday_5=models.BooleanField()
    weekday_6=models.BooleanField()
    weekday_7=models.BooleanField()
    weather_status_Klart=models.BooleanField()
    weather_status_Moln=models.BooleanField()
    weather_status_Regn=models.BooleanField()
    weather_status_Sno=models.BooleanField()


class Actual_Sold(models.Model):
    date=models.CharField(max_length=10, primary_key=True)
    sold=models.IntegerField()

    class Meta:
        db_table='actual_sales'
