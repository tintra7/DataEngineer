import pandas as pd
import os
from dotenv import load_dotenv
from datetime import date
from trino.dbapi import connect
from minio import Minio
from OCR_app import Model

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
ENDPOINT = "localhost:9000"

minio_client = Minio(ENDPOINT,
                      access_key=MINIO_ACCESS_KEY,
                      secret_key=MINIO_SECRET_KEY,
                      secure=False)
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

def read_data_by_date(
        table,
        year=str(date.today().year), 
        month=str(date.today().month), 
        day=str(date.today().day)
    ):
    print("Read data from {table}".format(table=table))
    df = pd.read_parquet(f"s3://datalake/{table}/year={year}/month={month}/day={day}",
                    storage_options={
                        "key": MINIO_ACCESS_KEY,
                        "secret": MINIO_SECRET_KEY,
                        "client_kwargs": {"endpoint_url": "http://localhost:9000/"}
                    })
    return df


def parse_papernote(
        year=str(date.today().year), 
        month=str(date.today().month), 
        day=str(date.today().day)
    ):
    list_obj = minio_client.list_objects("datalake", prefix=f"PaperNote/year={year}/month={month}/day={day}", recursive=True)
    dateTime_templates = ['Accepted at', 'Completed at', 'Boarded at', 'Picked up at']
    customer_templates = ['Name', 'Address', 'Phone', 'Email']
    order_templates = ['Name', 'Price', 'Trip type']
    staff_templates = ['Name', 'Phone', 'Email', "StaffID", "Store"]
    columns = dateTime_templates + customer_templates + order_templates + staff_templates
    df = pd.DataFrame(columns=columns)
    model = Model()
    count = 1
    for obj in list_obj:
        if count == 100:
            break
        count += 1
        img = obj.object_name
        path = img.split("/")
        number = path[-1][11:-4]
        print(number)
        if number == "124":
            continue

        response = minio_client.get_object(BUCKET_NAME, img)
        
        model.load_image(response=response)
        json = model.detect_ocr()
        json_flat = {}
        for i in json:
            json_flat.update(i)
        ls = [json_flat.get(i+':') for i in columns]
        df.loc[len(df.index)] = ls

    return df

# Join table and select feature for report and visualize

def transform_papernote(df_papernote):
    dateTime_templates = ['Accepted at', 'Completed at', 'Boarded at', 'Picked up at']
    for i in dateTime_templates:
        df_papernote[i] = pd.to_datetime(df_papernote[i])
    df_papernote = df_papernote.drop(['Address', 'Phone', 'Email', 'Name', 'Name', 'Phone', 'Email'], axis=1)
    df_papernote["Price"] = df_papernote["Price"].str[1:]
    df_papernote["Price"] = pd.to_numeric(df_papernote["Price"])
    df_papernote["ShipType"] = df_papernote['Trip type'].apply(lambda x: 0 if x == "Round" else 1)
    df_papernote = df_papernote.drop("Trip type", axis=1)
    df_papernote.rename(columns={'Accepted at': 'accepted_at', 
                             'Completed at': 'boarded_at',
                             'Boarded at': 'picked_up_at',
                             'Picked up at': 'completed_at',
                             'ShipType': 'shiptype',
                             "Price": "price",
                             'Store': "storename"}, inplace=True)
    return df_papernote


def create_cancel_report(cur, df_shipping, df_order, df_store):
    print("Creating cancel report")
    df = df_shipping.merge(df_shippingservice, how="inner", left_on="serviceid", right_on="id")
    df = df[["order_id", "cancelled_at", "servicename"]]
    df = df.merge(df_order[["id","storeid"]], left_on="order_id", right_on="id")
    df = df.merge(df_store, left_on="storeid", right_on="id")
    df = df.drop(["id_x", "id_y", "storeid"], axis=1)
    df = df.dropna(axis=0)
    df.cancelled_at = df['cancelled_at'].dt.time
    df = df.drop("stt", axis=1)
    cur.execute("DROP TABLE IF EXISTS iceberg.shipping_report.cancel_report")
    query = """CREATE TABLE IF NOT EXISTS iceberg.shipping_report.cancel_report(
    order_id varchar,
    cancelled_at time(6),
    servicename varchar,
    street varchar,
    storename varchar,
    city varchar
    )"""
    cur.execute(query)
    for i in range(len(df)):
        order_id = df.iloc[i]["order_id"]
        cancelled_at = df.iloc[i]["cancelled_at"]
        servicename = df.iloc[i]["servicename"]
        street = df.iloc[i]["street"]
        storename = df.iloc[i]["storename"]
        city = df.iloc[i]["city"]
        
        
        query = f"INSERT INTO iceberg.shipping_report.cancel_report VALUES ('{order_id}',TIME '{cancelled_at}', '{servicename}', '{street}', '{storename}', '{city}')"
        cur.execute(query)


def create_shipping_report(cur ,df_papernote, df_shipping, df_shippingservice, df_order, df_store):

    print("Creating shipping report")
    df = df_shipping[df_shipping['completed_at'].notnull()]
    df = df.drop("cancelled_at", axis=1)
    df = df[['accepted_at', 'boarded_at', 'picked_up_at', 
         'completed_at', 'shiptype', 'order_id', 'serviceid']]
    df = df.merge(df_shippingservice, how="inner", left_on="serviceid", right_on="id")
    df = df.drop(["serviceid", "serviceprovider", "stt"], axis=1)
    df = df.merge(df_order, how="inner", left_on="order_id", right_on='id')
    df = df.drop(['order_id', 'id_x', 'id_y', 'customername', 'created', 'stt', 'orderdetail'], axis=1)
    df = df.merge(df_store, left_on="storeid", right_on="id")
    df = df.drop(['storeid', 'id', 'street', 'city', 'stt'], axis=1)
    shipping_report = pd.concat([df, df_papernote], join="outer", axis=0)
    for i in shipping_report.columns[:4]:
        shipping_report[i] = pd.to_datetime(shipping_report[i])
    shipping_report['duration'] = abs((shipping_report['completed_at'] - shipping_report['boarded_at']).dt.total_seconds() / 3600)
    shipping_report['servicename'] = shipping_report['servicename'].fillna("Staff")
    shipping_report['StaffID'] = shipping_report['StaffID'].fillna("Service")
    cur.execute("DROP TABLE IF EXISTS iceberg.shipping_report.shipping")
    query = """CREATE TABLE IF NOT EXISTS iceberg.shipping_report.shipping(
                accepted_at timestamp(6),
                boarded_at timestamp(6),
                picked_up_at timestamp(6),
                completed_at timestamp(6),
                shiptype int,
                servicename varchar,
                price real,
                storename varchar,
                StaffID varchar,
                duration real
            )"""
    cur.execute(query)
    for i in range(len(shipping_report)):
        accepted_at = shipping_report.iloc[i]["accepted_at"]
        boarded_at = shipping_report.iloc[i]["boarded_at"]
        picked_up_at = shipping_report.iloc[i]["picked_up_at"]
        completed_at = shipping_report.iloc[i]["completed_at"]

        shiptype = shipping_report.iloc[i]["shiptype"]
        servicename = shipping_report.iloc[i]["servicename"]
        price = shipping_report.iloc[i]["price"]
        storename = shipping_report.iloc[i]["storename"]

        StaffID = shipping_report.iloc[i]["StaffID"]
        duration = shipping_report.iloc[i]["duration"]

        query = f"INSERT INTO iceberg.shipping_report.shipping VALUES (TIMESTAMP '{accepted_at}',TIMESTAMP '{boarded_at}', TIMESTAMP '{picked_up_at}',TIMESTAMP '{completed_at}',{shiptype}, '{servicename}', {price}, '{storename}', '{StaffID}',{duration})"
        cur.execute(query)
        

def create_papernote(cur, df_papernote):
    print("Creating papernote report")
    cur.execute("DROP TABLE IF EXISTS iceberg.shipping_report.paper_note")
    query = """CREATE TABLE IF NOT EXISTS iceberg.shipping_report.paper_note(
            accepted_at timestamp(6),
            boarded_at timestamp(6),
            picked_up_at timestamp(6),
            completed_at timestamp(6),
            price real,
            StaffID varchar,
            storename varchar,
            shiptype int)
            """
    cur.execute(query)
    for i in range(len(df_papernote)):
        accepted_at = df_papernote.iloc[i]["accepted_at"]
        boarded_at = df_papernote.iloc[i]["boarded_at"]
        picked_up_at = df_papernote.iloc[i]["picked_up_at"]
        completed_at = df_papernote.iloc[i]["completed_at"]

        shiptype = df_papernote.iloc[i]["shiptype"]
        price = df_papernote.iloc[i]["price"]
        storename = df_papernote.iloc[i]["storename"]
        StaffID = df_papernote.iloc[i]["StaffID"]

        query = f"INSERT INTO iceberg.shipping_report.paper_note VALUES (TIMESTAMP '{accepted_at}',TIMESTAMP '{boarded_at}', TIMESTAMP '{picked_up_at}',TIMESTAMP '{completed_at}', {price}, '{StaffID}', '{storename}',{shiptype})"
        cur.execute(query)


if __name__ == "__main__":

    df_product = read_data(table="Product")
    df_store = read_data(table="Store")
    df_account = read_data(table="Account")
    df_order = read_data(table="Order")
    df_shipping = read_data(table="Shipping")
    df_shippingservice = read_data(table="ShippingService")
    df_papernote = parse_papernote(day=2)
    df_papernote = transform_papernote(df_papernote.copy())

    conn = connect(
        host="localhost",
        port=8080,
        user="admin",
        catalog="iceberg",
    )
    cur = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS iceberg.shipping_report with (LOCATION = 's3a://lakehouse/')")
    create_cancel_report(cur=cur, df_shipping=df_shipping, df_order=df_order, df_store=df_store)
    create_shipping_report(cur=cur, df_papernote=df_papernote, df_shipping=df_shipping, df_shippingservice=df_shippingservice, df_order=df_order, df_store=df_store)
    create_papernote(cur=cur, df_papernote=df_papernote)
    cur.close()