import pandas as pd
import os
from dotenv import load_dotenv
from datetime import date
from trino.dbapi import connect

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

bucket = "lakehouse"
# Extract data from minio storage
def read_data(table):
    print("Read data from {table}".format(table=table))
    df = pd.read_parquet(f"s3://datalake/{table}".format(table=table),
                    storage_options={
                        "key": MINIO_ACCESS_KEY,
                        "secret": MINIO_SECRET_KEY,
                        "client_kwargs": {"endpoint_url": "http://localhost:9000/"}
                    }).drop(['year', 'month', 'day'], axis=1)
    return df

# Join table and select feature for report and visualize
df_product = read_data(table="Product")
df_store = read_data(table="Store")
df_account = read_data(table="Account")
df_order = read_data(table="Order")
df_shipping = read_data(table="Shipping")
df_shippingservice = read_data(table="ShippingService")

df = df_shipping.merge(df_shippingservice, how="inner", left_on="serviceid", right_on="id")
df = df[["order_id", "accepted_at", "boarded_at", "picked_up_at", "completed_at", "cancelled_at", "servicename"]]
df = df.merge(df_order[["id", "price"]], left_on="order_id", right_on="id")
df = df.drop(["order_id", "id"], axis=1)
# Create connection to Trino
conn = connect(
    host="localhost",
    port=8080,
    user="admin",
    catalog="iceberg",
)
cur = conn.cursor()
cur.execute(f"CREATE SCHEMA IF NOT EXISTS iceberg.shipping_report with (LOCATION = 's3a://{bucket}/shipping_report/')")
query = """CREATE TABLE IF NOT EXISTS iceberg.shipping_report.order_by_service(
    accepted_at timestamp(6),
    boarded_at timestamp(6),
    picked_up_at timestamp(6),
    completed_at timestamp(6),
    cancelled_at timestamp(6),
    servicename varchar,
    price int
)"""
cur.execute(query)

# Load data to Minio by Trino
for i in range(len(df)):
    accepted_at = df.iloc[i]["accepted_at"]
    boarded_at = df.iloc[i]["boarded_at"]
    picked_up_at = df.iloc[i]["picked_up_at"]
    completed_at = df.iloc[i]["completed_at"]
    cancelled_at = df.iloc[i]["cancelled_at"]
    servicename = df.iloc[i]["servicename"]
    price = df.iloc[i]["price"]
    
    if str(completed_at) == "NaT":
        query = f"INSERT INTO iceberg.shipping_report.order_by_service VALUES (TIMESTAMP '{accepted_at}',TIMESTAMP '{boarded_at}', TIMESTAMP '{picked_up_at}', NULL, TIMESTAMP'{cancelled_at}', '{servicename}', {price})"
        cur.execute(query)
    if str(cancelled_at) == "NaT":
        query = f"INSERT INTO iceberg.shipping_report.order_by_service VALUES (TIMESTAMP '{accepted_at}',TIMESTAMP '{boarded_at}', TIMESTAMP '{picked_up_at}', TIMESTAMP '{completed_at}', NULL, '{servicename}', {price})"
        cur.execute(query)

cur.close()