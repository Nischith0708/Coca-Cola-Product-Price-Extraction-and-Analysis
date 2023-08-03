import pandas as pd
import mysql.connector
from fastapi import FastAPI
import shutil
import json
from typing import Optional

original_file = 'output.csv'
duplicate_file = 'output_mod.csv'
shutil.copyfile(original_file, duplicate_file)

data = pd.read_csv(duplicate_file)
column_name = 'Price'
data[column_name] = data[column_name].str.replace(" 円", '')
data.to_csv(duplicate_file, index=False)
df = pd.read_csv('output_mod.csv')

df['Binary'] = df['Price'].apply(lambda x: "1" if int(x) != 0 else "0")

# Add the 'CLIENT' column with the value 'COKE'
df['CLIENT'] = 'COKE'

df.to_csv('output_mod.csv', index=False)

data = pd.read_csv('output_mod.csv')

database_name = "Price_Extraction"
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Appiappi12345",
    database="Price_Extraction"
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()
cursor.execute(f"use {database_name}")

create_table_query = '''
    CREATE TABLE IF NOT EXISTS output_sorted (
        Date VARCHAR(255),
        Links VARCHAR(255),
        Brands VARCHAR(255),
        Price VARCHAR(255),
        IsBinary VARCHAR(255),
        CLIENT VARCHAR(255)
    )
'''
cursor.execute(create_table_query)
cursor.execute('truncate table output_sorted')

# Insert data into the table
insert_query = '''
    INSERT INTO output_sorted (Date, Links, Brands, Price, IsBinary, CLIENT)
    VALUES (%s, %s, %s, %s, %s, %s)
'''

for _, row in data.iterrows():
    row_data = (row['Date'], row['Links'], row['Brands'], row['Price'], row['Binary'], row['CLIENT'])
    cursor.execute(insert_query, row_data)

cursor.close()
connection.commit()
cursor = connection.cursor()
app = FastAPI()


@app.get("/fetch-data")
async def fetch_data(client: Optional[str] = None):
    if client and client != 'COKE':
        return {"error": "Invalid client provided. Only 'COKE' is allowed."}

    cursor.execute("SELECT * FROM output_sorted")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        row_data = {}
        row_data["Dates"] = row[0]
        row_data["Links"] = row[1]
        row_data["Brands"] = row[2]
        row_data["Price"] = row[3]
        row_data['Binary'] = row[4]
        row_data['CLIENT'] = row[5]
        data.append(row_data)

    cursor.close()
    connection.commit()
    connection.close()
    json_data = {"data": data}
    with open("output.json", "w") as file:
        json.dump(json_data, file)

    return json_data


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using uvicorn
    uvicorn.run("JSON_FORMAT:app", host="0.0.0.0", port=8000)
