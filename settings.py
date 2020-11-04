import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DATABASES = {
#     'default': {
#         # Database driver
#         'ENGINE': 'django.db.backends.mysql',
#         # Replace below with Database Name if using other database engines
#         'NAME': "dataakdb"
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataak',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
INSTALLED_APPS = (
    'db',
)

"""
To connect to an existing postgres database, first:
pip install django psycopg2
then overwrite the settings above with:

"""

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = '6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa'