import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hejsan00",
  database="products"
)

def extract_data_from_csv():
    df = pd.read_csv('../data/grouped.csv')
    for index, row in df.iterrows():
        date = row['datum']
        ingredient_name = row['ingredient_name']
        ingredient_amount = row['ingredient_amount']
    print(df)


def create_tables(ingredient_names):
    cursor = mydb.cursor()
    for name in ingredient_names:
        table_name = name.lower().replace(' ', '_')
        cursor.execute(f"CREATE TABLE {table_name} (date DATE, amount FLOAT)")
    mydb.commit()



def populate_database():
    df = pd.read_csv('../data/grouped.csv')
    ingredient_names = set(df['ingredient_name'])
    create_tables(ingredient_names)
    cursor = mydb.cursor()
    for index, row in df.iterrows():
        date = row['datum']
        ingredient_name = row['ingredient_name']
        ingredient_amount = row['ingredient_amount']
        table_name = ingredient_name.lower().replace(' ', '_')
        query = f"INSERT INTO {table_name} (date, amount) VALUES (%s, %s)"
        cursor.execute(query, (date, ingredient_amount))
    mydb.commit()

populate_database()