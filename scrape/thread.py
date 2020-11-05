from db.models import Community, Thread
import re
from logger import Logger
from .request import send_request
from django.core.exceptions import MultipleObjectsReturned

logger = Logger.__call__().get_logger()

"""
This function create threads of each community.
Note that this function also create these threads.
"""


def create_thread(url, cookie):
    community = Community.objects.all()
    pattern_finding = re.compile(
        r"<span> <span class=\" subject_old\" id=\"tid_[0-9]{1,}\"><a href=\"(.*)\">(.*)</a></span>")
    for com in community:
        request = send_request(f"{url}/{com.url}", cookie)
        if request.text.find("<!-- start: forumdisplay_thread -->") != -1:
            index_of_begin = request.text.find("<!-- start: forumdisplay_thread -->")
            sub_text = request.text[index_of_begin::]
            found = re.findall(pattern_finding, sub_text)[0]
            try:
                new_thread, status = Thread.objects.get_or_create(title=found[1], url=found[0], community=com)
            except MultipleObjectsReturned:
                logger.error(f"There is more than one thread with {found[1]} title")
                # This exception should be handel due to business logic
            logger.info(f"new thread created. the title is: {new_thread.title} and url is : {new_thread.url}")
        else:
            logger.info(f"there is no threads for this {com.title} title")

    return "new threads created!"
