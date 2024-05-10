import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import sys
from datetime import date
import string
import random

load_dotenv()

# Define constant
URL = os.environ.get("URL")
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = 5432
DATABASE = os.environ.get("DATABASE") 

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

BUCKET_NAME = "datalake"
ENDPOINT = "http://localhost:9000/"

# Connect to remote postgres database
def connect():
    conn = None
    try:
        print('Connecting')
        conn = psycopg2.connect(dbname=DATABASE, user=USER_NAME, password=PASSWORD, host=HOST, port=PORT)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print('All good, Connection successful!')
    return conn
    
# Create connection
conn = connect()

# Store table in pandas dataframe
def sql_to_dataframe(conn, query, columns):
    cur = conn.cursor()
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}" )
        cur.close()
        return 1
    tuple_list = cur.fetchall()
    cur.close()
    df = pd.DataFrame(tuple_list, columns=columns)
    return df

# Read data from database
def read_from_database(table):
    # Get the lasted record of table 
    # df = pd.read_parquet(f"s3://datalake/{table}",
    #                 storage_options={
    #                     "key": MINIO_ACCESS_KEY,
    #                     "secret": MINIO_SECRET_KEY,
    #                     "client_kwargs": {"endpoint_url": "http://localhost:9000/"}
    #                 }).drop(['year', 'month', 'day'], axis=1)
    
    # stt = max(df['stt'])
    stt = 0
    print("Reading data from", table)
    if table == "Account":
        columns = ["id", "firstname", "lastname", "email", "phone", "created", "stt", "staffid", "storeid"]
        query = 'SELECT * FROM public."Account" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)

    if table == "Order":
        columns = ["id", "customername", "storeid", "created", "stt", "orderdetail", "price"]
        query = 'SELECT * FROM public."Order" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)

    if table == "Product":
        columns = ["id", "productname", "price", "stt"]
        query = 'SELECT * FROM public."Product" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)

    if table == "Store":
        columns = ["id", "street", "storename", "city", "stt"]
        query = 'SELECT * FROM public."Store" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)
    
    if table == "ShippingService":
        columns = ["id", "serviceprovider", "servicename", "stt"]
        query = 'SELECT * FROM public."ShippingService" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)

    if table == "Shipping":
        columns = ["id", "accepted_at", "boarded_at", "picked_up_at", "completed_at", "cancelled_at", "charged", "serviceid", "order_id", "stt", 'shiptype']
        query = 'SELECT * FROM public."Shipping" WHERE stt > {stt}'.format(stt=stt)
        return sql_to_dataframe(conn, query=query, columns=columns)

# Load dato to Minio object storage
def load_data_to_minio(tables): 
    # Partition as year/month/day
    year = str(date.today().year)
    month = str(date.today().month)
    day = str(date.today().day)
    N = 16 #len of table name
    table_name = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + "_") for _ in range(N))

    for table in tables:
        df = read_from_database(table)
        df.to_parquet(f"s3://datalake/{table}/year={year}/month={month}/day=9/{table_name}.parquet".format(table_name=table_name),
                    storage_options={
                        "key": MINIO_ACCESS_KEY,
                        "secret": MINIO_SECRET_KEY,
                        "client_kwargs": {"endpoint_url": "http://localhost:9000/"}
                    })
        
if __name__ == "__main__":
    tables = ["Account", "Shipping", "Order", "Product", "Store", "ShippingService"]
    load_data_to_minio(tables=tables)