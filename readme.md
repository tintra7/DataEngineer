### Introduction 

This is my team's Data Enineering project for Data lakehouse. 

To run this project on your machine, you have to clone it and simply run a

Install Postgresql server in your local machine or connect to a remote server

Create a file names it ".env" and add nessesary enviroment variable

```bash
docker compose up -d
```

(Optional) Create your virtual enviroment
```bash
python -m venv env
env\Scripts\activate.bat
```

Install packages
```bash
pip install -r requirements.txt
```

If this is your first time run this project, please set stt = 0 and comment the code read data from Minio in loader.py file

```bash
python loader.py
python load_image.py
python transformation.py
```