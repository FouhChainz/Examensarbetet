import requests, json

#API Key from OpenWeatherMap
api_key="8e617af5b1fd73c2088b4c95516c9eaa"

# base_url variable to store url
base_url="http://api.openweathermap.org/data/2.5/weather?"

#Input city name
#city_name=input("Enter city name : ") --Possibility to input city every time? Maybe have this in set up

# complete_url variable to store all added functionalities cleanly
complete_url=base_url + \
             "appid=" + api_key + \
             "&q=gothenburg,SE" + \
             "&lang=se" + \
             "&units=metric"

# get method of requests module
# return response object
response=requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x=response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y=x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature=y["temp"]

    # store the value of "weather"
    # key in variable z
    z=x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description=z[0]["description"]
    weather_status=z[0]["main"]

    # print following values
    print(" Temperatur (C) = " +
          str(current_temperature) +
          "\n Väder Status = " +
          str(weather_status))



else:
    print(" City Not Found ")
