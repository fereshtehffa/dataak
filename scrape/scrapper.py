import requests
import re


class Login:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def login(self):
        base = requests.get(self.url)
        auth_key = re.findall('var my_post_key = \"(.*?)\";', base.text)[0]
        first_cookie = base.cookies.get_dict()
        first_cookie["loginattempts"] = "1"
        data = {
            "url": f"{self.url}/index.php",
            "action": "do_login",
            "submit": "Login",
            "quick_login": "1",
            "quick_username": f"{self.username}",
            "quick_password": f"{self.password}",
            'my_post_key': auth_key,
        }
        r = requests.post(f"{self.url}/member.php", data=data, cookies=first_cookie)
        return r.cookies.get_dict()


