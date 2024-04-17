import pandas as pd
import os
from dotenv import load_dotenv
from datetime import date
import requests
from minio import Minio
from io import BytesIO


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

url = "https://lakehouse-b871d5ac2bac.herokuapp.com/paper-notes"

respone = requests.get(url)

image_urls = respone.json()['image_urls']


for i, image_url in enumerate(image_urls):
    # Fetch the image from the URL
    response = requests.get(image_url)
    year = str(date.today().year)
    month = str(date.today().month)
    day = str(date.today().day)
    path = "/PaperNote/" + f"year={year}/month={month}/day={day}/"
    name = path + f"paper_note{i}.png"
    # found = minio_client.bucket_exists(bucket_name=BUCKET_NAME)
    # if not found:
    #     minio_client.make_bucket(path)
    #     print("Created bucket", path)
    # else:
    #     print("Bucket", path, "already exists")
    if response.status_code == 200:
        # Upload the image data to MinIO
        image_data = BytesIO(response.content)
        file_size = len(response.content)
        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=name,  # Change the object name as needed
            data=image_data,
            length=file_size,
            content_type="image/png"

        )
        print("Image uploaded successfully.")
    else:
        print("Failed to fetch the image from the URL.")