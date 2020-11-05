import sys
import os
sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from scrape.scrapper import Login
from scrape.community import create_community
from scrape.thread import create_thread
from scrape.comment import create_comment

#
login_obj = Login("https://forum.dataak.com/", "crawling", "32145713")
cookie = login_obj.login()
"""
the order of functions is important!

"""
#TODO All functions needs exception handeling

print(create_community(cookie, "https://forum.dataak.com/index.php"))
# print(create_thread("https://forum.dataak.com/", cookie))
# print(create_comment("https://forum.dataak.com/", cookie))