import requests
from db.models import Thread, Comment, User
import re
from django.core.exceptions import MultipleObjectsReturned
from .request import send_request
from logger import Logger

logger = Logger.__call__().get_logger()


def create_comment(url, cookie):

    threads = Thread.objects.all()
    pattern_url_author = re.compile(r"<a href=\"https://forum\.dataak\.com/(.*)\"><span style=\"color: green;\">")
    for thread in threads:
        request = send_request(f"{url}/{thread.url}", cookie)
        index_of_begin = request.text.find("<!-- end: postbit_avatar -->")
        sub_text = request.text[index_of_begin::]
        found = re.findall(pattern_url_author, sub_text)[0]
        author_name = re.findall("<em>(.*)</em>", sub_text)[0]
        try:
            user, status = User.objects.get_or_create(name=author_name, url=found)
        except MultipleObjectsReturned:
            logger.error(f"There is more than one User with {author_name} name")
            # This exception should be handel due to business logic
        logger.info(f"the author for {thread.title} is ---> {user.name}")
        thread.author = user
        thread.save()
        sub_text = sub_text[find_nth(sub_text, "<!-- end: postbit_posturl -->", 2)::]
        # next step
        pattern_of_comments = re.compile(r"<a href=\"https://forum\.dataak\.com/(.*)\">(.*)</a>")
        sub_text = sub_text[:sub_text.find("<!-- start: footer_contactus -->"):]
        if sub_text.count("<!-- end: postbit_posturl -->"):
            find_comment = re.findall(pattern_of_comments, sub_text)
            for item in find_comment:
                try:
                    user, status = User.objects.get_or_create(name=item[1], url=item[0])
                except MultipleObjectsReturned:
                    logger.error(f"There is more than one User with {item[1]} name")
                    # This exception should be handel due to business logic
                Comment.objects.get_or_create(user=user, thread=thread)
                logger.info(f"the comment for {thread.title} and the user who wrote it is:--->  {user.name}")
    return "comments created!"


def find_nth(text, needle, n):
    start = text.find(needle)
    while start >= 0 and n > 1:
        start = text.find(needle, start + len(needle))
        n -= 1
    return start