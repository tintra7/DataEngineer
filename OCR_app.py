import cv2
import numpy as np
from paddleocr import PaddleOCR
from fuzzywuzzy import process
from PIL import Image

def fuzzy_match(text, options):
    
    best_match, score = process.extractOne(text, options)
    if score >= 90:
        return best_match
    else:
        return None

def parse_shipping_info(text):
    
    lines = text
    print(lines)
    # Initialize variables to store information
    dateTimeDetails = {}
    customerDetails = {}
    orderDetails = {}
    staffDetails = {}

    # Define templates for each section
    dateTime_templates = ['Accepted at:', 'Completed at:', 'Boarded at:', 'Picked up at:']
    customer_templates = ['Name:', 'Address:', 'Phone:', 'Email:']
    order_templates = ['Name:', 'Price:', 'Trip type:']
    staff_templates = ['Name:', 'Phone:', 'Email:', "StaffID:", "Store:"]

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
            

            matched_prop = fuzzy_match(line, dateTime_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()

                d = line.split(" ")
                time_hour = d[-2] + d[-1]
                time_date = d[-3]
                
                dateTimeDetails[key] = time_hour + ' ' + time_date
        elif current_section == 'customerDetails':
            matched_prop = fuzzy_match(line, customer_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                if key == "Name:":
                    key = "cusName:"
                customerDetails[key] = value
        elif current_section == 'orderDetails':
            matched_prop = fuzzy_match(line, order_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                if key == "Name:":
                    key = "ordName:"
                orderDetails[key] = value
        elif current_section == 'staffDetails':
            matched_prop = fuzzy_match(line, staff_templates)
            if matched_prop:
                key, value = matched_prop.strip(), line.split(":")[1].strip()
                if key == "Name:":
                    key = "staffName:"
                staffDetails[key] = value

    return dateTimeDetails, customerDetails, orderDetails, staffDetails

class Model:
    def __init__(self):
        self.image = None
        self.ocr = PaddleOCR(use_angle_cls=True,lang="en") # The model file will be downloaded automatically when executed for the first time
    def load_image(self, response):
        image_array = np.frombuffer(response.data, dtype=np.uint8)
        self.image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.image

    def detect_ocr(self):
        if self.image is not None:
            result = self.ocr.ocr(self.image, cls=True)
            # Recognition and detection can be performed separately through parameter control
            # result = ocr.ocr(img_path, det=False)  Only perform recognition
            # result = ocr.ocr(img_path, rec=False)  Only perform detection
            # Print detection frame and recognition result
                        
            result = result
            image = Image.fromarray(self.image) 
            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            # im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
            # im_show = Image.fromarray(im_show)
            # im_show.save('result.jpg')
            text = []
            for line in result:
                text.append(line[1][0])
                # print(line[1][0])
            dateTimeDetails, customerDetails, orderDetails, staffDetails = parse_shipping_info(text)
            # print(dateTimeDetails, customerDetails, orderDetails, staffDetails)

            return dateTimeDetails, customerDetails, orderDetails, staffDetails
        
