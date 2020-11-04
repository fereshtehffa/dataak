import requests
import re
from db.models import Community


def create_community(cookie, url):
    request = requests.get(url, cookies=cookie)
    text = request.text
    regex_for_community = r"<strong><a href=\"forumdisplay\.php\?fid=[0-9]{1,}\">(.*)</a></strong><div class=\".*\">"
    pattern_community = re.compile(regex_for_community)
    regex_for_sub_communities = r"class=\"subforumicon subforum_minioff ajax_mark_read\" id=\"mark_read_[0-9]{1,}\"></div><a href=\"forumdisplay\.php\?fid=[0-9]{1,}\" title=\"\">([^</a>]*)"
    pattern_sub_community = re.compile(regex_for_sub_communities)
    communities = re.findall(pattern_community, text)
    print("comunities", communities)
    sub_communities = re.findall(pattern_sub_community, text)
    print("sub:", sub_communities)
    if not communities:
        raise Exception("There is no cummunity!")
    for com in communities:
        url_of_community = re.findall(f"<a href=\"(.*)\">{com}</a>", text)[0]
        new_community, status = Community.objects.get_or_create(title=com, url=url_of_community)
        print(f"community is {new_community.title} and the url is: {new_community.url}")
        for sub in sub_communities:
            index_of_begin = text.find(com)
            sub_text = text[index_of_begin::]
            index_of_end = text[index_of_begin::].find("</td>")
            if not Community.objects.filter(title=sub).exists() and sub_text[:index_of_end:].rfind(sub) != -1:
                url_of_sub = re.findall(f"<a href=\"([^<]*)\" title=\"\">{sub}</a>", sub_text)[0]
                new = Community.objects.create(title=sub, parent=new_community, url=url_of_sub)
                print(
                    f"com: {new_community.title} and the sub is :{new.title}----> parent is {new.parent.title}, url is : {new.url}")
    return "Add communities successfully"
