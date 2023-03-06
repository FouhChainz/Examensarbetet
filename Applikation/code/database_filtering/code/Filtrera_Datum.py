import pandas as pd

maxChars=10

df = pd.read_csv(r'/Users/christianzhaco/PycharmProjects/Examensarbete/database_filtering/dag_filtrerad.csv')


df.replace(['Clouds'], 'Moln',inplace=True,regex=True)
df.replace(['Rain'], 'Regn',inplace=True,regex=True)
df.replace(['Clear'], 'Klart',inplace=True,regex=True)
df.replace(['Snow'], 'Snö',inplace=True,regex=True)
print(df)

df.to_csv('weather_data.csv',index=False)
