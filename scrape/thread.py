import requests
from db.models import Community, Thread
import re


def create_thread(url, cookie):
    community = Community.objects.all()
    pattern_finding = re.compile(
        r"<span> <span class=\" subject_old\" id=\"tid_[0-9]{1,}\"><a href=\"(.*)\">(.*)</a></span>")
    # TODO checking for duplication threads
    for com in community:
        request = requests.get(f"{url}/{com.url}", cookies=cookie)
        if request.text.find("<!-- start: forumdisplay_thread -->") != -1:
            index_of_begin = request.text.find("<!-- start: forumdisplay_thread -->")
            sub_text = request.text[index_of_begin::]
            found = re.findall(pattern_finding, sub_text)[0]
            new_thread, status = Thread.objects.get_or_create(title=found[1], url=found[0], community=com)
            print(f"new thread created. the title is: {new_thread.title} and url is : {new_thread.url}")

    return "new threads created!"
