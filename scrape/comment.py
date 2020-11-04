import requests
from db.models import Thread, Comment, User
import re


def create_comment(url, cookie):

    # TODO code needs refactoring

    threads = Thread.objects.all()
    pattern_url_author = re.compile(r"<a href=\"https://forum\.dataak\.com/(.*)\"><span style=\"color: green;\">")
    for thread in threads:
        request = requests.get(f"{url}/{thread.url}", cookies=cookie)
        index_of_begin = request.text.find("<!-- end: postbit_avatar -->")
        sub_text = request.text[index_of_begin::]
        found = re.findall(pattern_url_author, sub_text)[0]
        author_name = re.findall("<em>(.*)</em>", sub_text)[0]
        try:
            user = User.objects.get_or_create(name=author_name, url=found)
        except:
            pass
        thread.author = user[0]
        print(f"the author for {thread.title} is ---> {user[0].name}")
        thread.save()
        sub_text = sub_text[sub_text.find("<!-- end: postbit_posturl -->")::]
        sub_text = sub_text[sub_text.find("<!-- end: postbit_posturl -->")::]
        # next step
        pattern_of_comments = re.compile(r"<a href=\"https://forum\.dataak\.com/(.*)\">(.*)</a>")
        sub_text = sub_text[:sub_text.find("<!-- start: footer_contactus -->"):]
        count_of_comment = sub_text.count("<!-- end: postbit_posturl -->")
        if count_of_comment:
            find_comment = re.findall(pattern_of_comments, sub_text)
            for item in find_comment:
                try:
                    user = User.objects.get_or_create(name=item[1], url=item[0])
                except:
                    pass
                Comment.objects.get_or_create(user=user[0], thread=thread)
                print(f"the comment for {thread.title} :---> user: {user[0].name}")

    return "comments created!"
