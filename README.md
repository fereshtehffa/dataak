This is a simple scrapper to gather data from `https://forum.dataak.com/`.

This scrapper uses `django-orm` to connect to the database.
The default database engine is mysql, so it can be change in settings.py.
note that the security code should be considered in settings.py.
# Default database information
```
username: root
password: 123
address: 127.0.0.1
```

# How to run the app
1. Install requirements:
```
pip3 install -r requirements.txt
```
2. Make the migration
```
python3 manage.py migrate
```
3. Run the application
```
python3 main.py
```
