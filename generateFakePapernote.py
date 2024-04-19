from faker import Faker
import random
import datetime

fake = Faker()

staff_details = [
  {
    "firstname": "Lorreta",
    "lastname": "Thomas",
    "phone": "111-888-5555",
    "email": "lorreta.thomas@example.com",
    "staffid": "SD11",
    "storename": "SuperMart"
  },
  {
    "firstname": "Daisy",
    "lastname": "Frazier",
    "phone": "444-444-4444",
    "email": "daisy.frazier@example.com",
    "staffid": "SD06",
    "storename": "SuperMart"
  },
  {
    "firstname": "George",
    "lastname": "Smith",
    "phone": "555-444-9999",
    "email": "george.smith@example.com",
    "staffid": "SD23",
    "storename": "MegaMart"
  },
  {
    "firstname": "Ryan",
    "lastname": "Garcia",
    "phone": "666-777-8888",
    "email": "ryan.garcia@example.com",
    "staffid": "SD37",
    "storename": "MegaMart"
  },
  {
    "firstname": "Nancy",
    "lastname": "Shah",
    "phone": "444-333-2222",
    "email": "nancy.shah@example.com",
    "staffid": "SD22",
    "storename": "Grocery Warehouse"
  },
  {
    "firstname": "Vanessa",
    "lastname": "Daniel",
    "phone": "987-654-3210",
    "email": "vanessa.daniel@example.com",
    "staffid": "SD14",
    "storename": "Grocery Warehouse"
  },
  {
    "firstname": "Amanda",
    "lastname": "Love",
    "phone": "111-222-3333",
    "email": "amanda.love@example.com",
    "staffid": "SD13",
    "storename": "BigBox Store"
  },
  {
    "firstname": "Sophia",
    "lastname": "Rodriguez",
    "phone": "777-888-9999",
    "email": "sophia.rodriguez@example.com",
    "staffid": "SD38",
    "storename": "BigBox Store"
  },
  {
    "firstname": "Paige",
    "lastname": "Smith",
    "phone": "987-654-3210",
    "email": "paige.smith@example.com",
    "staffid": "SD03",
    "storename": "Corner Market"
  },
  {
    "firstname": "Emily",
    "lastname": "Cobb",
    "phone": "555-444-3333",
    "email": "emily.cobb@example.com",
    "staffid": "SD01",
    "storename": "Corner Market"
  },
  {
    "firstname": "Kimberly",
    "lastname": "Martin",
    "phone": "123-456-7890",
    "email": "kimberly.martin@example.com",
    "staffid": "SD21",
    "storename": "Neighborhood Market"
  },
  {
    "firstname": "Dana",
    "lastname": "Foster",
    "phone": "777-777-7777",
    "email": "dana.foster@example.com",
    "staffid": "SD17",
    "storename": "Neighborhood Market"
  },
  {
    "firstname": "Jacob",
    "lastname": "Kelly",
    "phone": "222-333-4444",
    "email": "jacob.kelly@example.com",
    "staffid": "SD02",
    "storename": "Discount Groceries"
  },
  {
    "firstname": "Brandon",
    "lastname": "Logan",
    "phone": "123-456-7890",
    "email": "brandon.logan@example.com",
    "staffid": "SD15",
    "storename": "Discount Groceries"
  },
  {
    "firstname": "Sarah",
    "lastname": "Anderson",
    "phone": "333-444-5555",
    "email": "sarah.anderson@example.com",
    "staffid": "SD34",
    "storename": "Budget Mart"
  },
  {
    "firstname": "Jessica",
    "lastname": "Bass",
    "phone": "444-444-4444",
    "email": "jessica.bass@example.com",
    "staffid": "SD07",
    "storename": "Budget Mart"
  },
  {
    "firstname": "John",
    "lastname": "Doe",
    "phone": "444-555-6666",
    "email": "john.doe@example.com",
    "staffid": "SD25",
    "storename": "Value Mart"
  },
  {
    "firstname": "Eugene",
    "lastname": "Gilbert",
    "phone": "888-888-8888",
    "email": "eugine.gilbert@example.com",
    "staffid": "SD05",
    "storename": "Value Mart"
  },
  {
    "firstname": "David",
    "lastname": "Brown",
    "phone": "666-777-8888",
    "email": "david.brown@example.com",
    "staffid": "SD29",
    "storename": "Quick Mart"
  },
  {
    "firstname": "Olivia",
    "lastname": "Lee",
    "phone": "999-000-1111",
    "email": "olivia.lee@example.com",
    "staffid": "SD40",
    "storename": "Quick Mart"
  },
  {
    "firstname": "Kelly",
    "lastname": "Crawford",
    "phone": "666-777-8888",
    "email": "kelly.crawford@example.com",
    "staffid": "SD16",
    "storename": "Bulk Bargains"
  },
  {
    "firstname": "John",
    "lastname": "Doe",
    "phone": "444-555-6666",
    "email": "john.doe@example.com",
    "staffid": "SD31",
    "storename": "Bulk Bargains"
  },
  {
    "firstname": "James",
    "lastname": "Hoffman",
    "phone": "111-222-3333",
    "email": "james.hoffman@example.com",
    "staffid": "SD19",
    "storename": "Bulk Bargains"
  },
  {
    "firstname": "Alice",
    "lastname": "Johnson",
    "phone": "111-222-3333",
    "email": "alice.johnson@example.com",
    "staffid": "SD32",
    "storename": "Bulk Bargains"
  },
  {
    "firstname": "Daniel",
    "lastname": "Martinez",
    "phone": "444-555-6666",
    "email": "daniel.martinez@example.com",
    "staffid": "SD35",
    "storename": "Bulk Bargains"
  },
  {
    "firstname": "Michael",
    "lastname": "Brown",
    "phone": "222-333-4444",
    "email": "michael.brown@example.com",
    "staffid": "SD33",
    "storename": "Discount Depot"
  },
  {
    "firstname": "Nicole",
    "lastname": "Cortez",
    "phone": "999-999-9999",
    "email": "nicole.cortez@example.com",
    "staffid": "SD18",
    "storename": "Discount Depot"
  },
  {
    "firstname": "Amanda",
    "lastname": "Knight",
    "phone": "333-222-1111",
    "email": "amanda.knight@example.com",
    "staffid": "SD20",
    "storename": "Super Savings"
  },
  {
    "firstname": "William",
    "lastname": "Lopez",
    "phone": "888-999-0000",
    "email": "william.lopez@example.com",
    "staffid": "SD39",
    "storename": "Super Savings"
  },
  {
    "firstname": "Carrol",
    "lastname": "Williams",
    "phone": "222-333-4444",
    "email": "carrol.williams@example.com",
    "staffid": "SD09",
    "storename": "Super Savings"
  },
  {
    "firstname": "Carmen",
    "lastname": "Holmes",
    "phone": "999-888-7777",
    "email": "carmen.holmes@example.com",
    "staffid": "SD04",
    "storename": "Value Foods"
  },
  {
    "firstname": "Emma",
    "lastname": "Thomas",
    "phone": "555-666-7777",
    "email": "emma.thomas@example.com",
    "staffid": "SD36",
    "storename": "Value Foods"
  },
  {
    "firstname": "Darren",
    "lastname": "Jackson",
    "phone": "555-555-5555",
    "email": "darren.jackson@example.com",
    "staffid": "SD10",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Elizabeth",
    "lastname": "Harris",
    "phone": "999-999-9999",
    "email": "elizabeth.harris@example.com",
    "staffid": "SD08",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Emma",
    "lastname": "Jones",
    "phone": "999-888-7777",
    "email": "emma.jones@example.com",
    "staffid": "SD30",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Joseph",
    "lastname": "Garrett",
    "phone": "666-666-6666",
    "email": "joseph.garrett@example.com",
    "staffid": "SD12",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Jason",
    "lastname": "Moore",
    "phone": "555-555-5555",
    "email": "jason.moore@example.com",
    "staffid": "SD24",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Emily",
    "lastname": "Smith",
    "phone": "777-888-9999",
    "email": "emily.smith@example.com",
    "staffid": "SD26",
    "storename": "Fresh Fare"
  },
  {
    "firstname": "Michael",
    "lastname": "Johnson",
    "phone": "123-456-7890",
    "email": "michael.johnson@example.com",
    "staffid": "SD27",
    "storename": "BigBox Store"
  },
  {
    "firstname": "Sarah",
    "lastname": "Williams",
    "phone": "222-333-4444",
    "email": "sarah.williams@example.com",
    "staffid": "SD28",
    "storename": "Discount Depot"
  }
]

def generate_fake_data():
    # Generate datetime details
    accepted_at = fake.date_time_between_dates(datetime_start=datetime.datetime(2024, 1, 1), datetime_end=datetime.datetime(2024, 4, 30))
    completed_at = accepted_at + datetime.timedelta(hours=random.randint(1, 4))
    boarded_at = completed_at + datetime.timedelta(minutes=random.randint(30, 120))
    picked_up_at = boarded_at + datetime.timedelta(minutes=random.randint(30, 120))

    # Generate customer details
    customer_name = fake.name()
    customer_address = fake.street_address()
    customer_phone = fake.phone_number()
    customer_email = fake.email()

    # Generate order details
    order_name = fake.word() + " " + fake.word()
    order_price = round(random.uniform(10, 100), 2)
    trip_type = random.choice(["Single", "Round"])

    # Select a random staff detail from the pre-generated list
    staff = random.choice(staff_details)
    
    return f"""Date time details :
Accepted at : {accepted_at.strftime('%Y-%m-%d %I:%M %p')}
Completed at : {completed_at.strftime('%Y-%m-%d %I:%M %p')}
Boarded at : {boarded_at.strftime('%Y-%m-%d %I:%M %p')}
Picked up at : {picked_up_at.strftime('%Y-%m-%d %I:%M %p')}

Customer details :
Name : {customer_name}
Address : {customer_address}
Phone : {customer_phone}
Email : {customer_email}

Order details :
Name : {order_name}
Price : ${order_price:.2f}
Trip type : {trip_type}

Staff details :
Name : {staff['firstname']} {staff['lastname']}
Phone : {staff['phone']}
Email : {staff['email']}
StaffID : {staff['staffid']}
Store : {staff['storename']}

//
"""

if __name__ == "__main__":
    with open("fake_data.txt", "w") as f:
        for _ in range(250):
            fake_data = generate_fake_data()
            f.write(fake_data)