# How to run

1. Clone repository
2. Install python 3 from [python.org](https://www.python.org/)
3. install requirements packages
 ```
 pip install -r requirements.txt
 ```
3. create database
 ```
 python create_db.py
 ```
4. Run using shell
 ```
 waitress-serve --listen=127.0.0.1:8080 wsgi:app      
 ```
   or
 ```
 python wsgi.py
 ```
You can change the host and port in settings.py