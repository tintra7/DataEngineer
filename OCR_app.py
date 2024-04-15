import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from paddleocr import PaddleOCR, draw_ocr
from fuzzywuzzy import process
from io import BytesIO
import pandas as pd
from numpy import random
import minio
import numpy
from PIL import Image
import os
import wget


MINIO_ACCESS_KEY = "DaV8J74cejp6LESX"
MINIO_SECRET_KEY = "hfO0XtELb7UDgZqCZ7fSsQCxIODE7LN1"
# Create the client
client = minio.Minio(
    endpoint="localhost:9000",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)
import json
import requests
response = requests.get("https://lakehouse-b871d5ac2bac.herokuapp.com/paper-notes")
image_list = json.loads(response.text)["image_urls"]
        # Put the object into minio
# client.put_object(
#             bucket_name="sample-lakehouse",
#             object_name="demo.feather", 
#             length=nb_bytes,
#             data=feather_output
#         )

def fuzzy_match(text, options):
    
    best_match, score = process.extractOne(text, options)
    if score >= 90:
        return best_match
    else:
        return None

def parse_shipping_info(text):
    
    lines = text

    # Initialize variables to store information
    dateTimeDetails = {}
    customerDetails = {}
    orderDetails = {}
    staffDetails = {}

    # Define templates for each section
    dateTime_templates = ['Accepted at:', 'Completed at:', 'Boarded at:', 'Picked up at:']
    customer_templates = ['Name:', 'Address:', 'Phone:', 'Email:']
    order_templates = ['Name:', 'Price:', 'Trip type:']
    staff_templates = ['Name:', 'Phone:', 'Email:']
    print(lines)
    current_section = None
    for line in lines:
        if 'date time details' in line.lower():
            current_section = 'dateTimeDetails'
        elif 'customer details' in line.lower():
            current_section = 'customerDetails'
        elif 'order details' in line.lower():
            current_section = 'orderDetails'
        elif 'staff details' in line.lower():
            current_section = 'staffDetails'
        elif current_section == 'dateTimeDetails':
            print(line.split(" "))

            matched_prop = fuzzy_match(line, dateTime_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()

                d = line.split(" ")
                time_hour = d[-2] + d[-1]
                time_date = d[-3]
                
                dateTimeDetails[key] = [time_hour, time_date]
        elif current_section == 'Customer Details':
            matched_prop = fuzzy_match(line, customer_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                customerDetails[key] = value
        elif current_section == 'orderDetails':
            matched_prop = fuzzy_match(line, order_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                orderDetails[key] = value
        elif current_section == 'staffDetails':
            matched_prop = fuzzy_match(line, staff_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                staffDetails[key] = value

    return dateTimeDetails, customerDetails, orderDetails, staffDetails
class Model:
    def __init__(self):
        self.image = None
        self.ocr = PaddleOCR(use_angle_cls=True,lang="en") # The model file will be downloaded automatically when executed for the first time
    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.image

    def detect_ocr(self):
        if self.image is not None:
            result = self.ocr.ocr(self.image, cls=True)
            # Recognition and detection can be performed separately through parameter control
            # result = ocr.ocr(img_path, det=False)  Only perform recognition
            # result = ocr.ocr(img_path, rec=False)  Only perform detection
            # Print detection frame and recognition result
                        
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    print(line)

            result = result
            image = Image.fromarray(self.image) 
            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
            im_show = Image.fromarray(im_show)
            # im_show.save('result.jpg')


            text = []
            for line in result:
                text.append(line[1][0])
                # print(line[1][0])
            dateTimeDetails, customerDetails, orderDetails, staffDetails = parse_shipping_info(text)
            print(dateTimeDetails, customerDetails, orderDetails, staffDetails)

            return im_show, dateTimeDetails, customerDetails, orderDetails, staffDetails

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Test")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton("Load Image")
        self.detect_button = QPushButton("Detect Text")

        self.getdata_button = QPushButton("Get data from API")

   

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.detect_button)
        self.layout.addWidget(self.getdata_button)
        self.load_button.clicked.connect(self.load_image)
        self.detect_button.clicked.connect(self.detect_ocr)
        self.getdata_button.clicked.connect(self.crawl_data)


    def display_image(self, image):
        if image is not None:
            image  = np.array(image)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.resize(600,400)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.jpg *.png *.bmp);;All Files (*)", options=options)
        if file_path:
            controller.load_image(file_path)

            client.fput_object("sample-lakehouse", file_path.split("/")[-1],file_path)

    def detect_ocr(self):
        result_img,_,_,_,_ = controller.detect_ocr()
        self.display_image(result_img)
    def crawl_data(self):

        if not os.path.exists("./ocr_img"):
            os.makedirs("./ocr_img") 
        for url in image_list:             #download all papernote image
            wget.download(url, "./ocr_img")
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_image(self, image_path):
        image = self.model.load_image(image_path)
        self.view.display_image(image)

    def detect_ocr(self):
        return self.model.detect_ocr()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())