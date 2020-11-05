from logger import Logger
from .request import send_request
import re
from db.models import Community

logger = Logger.__call__().get_logger()

"""
This function is for finding communities and also their sub communities.
note that it also saves communities and their sub communitis.
"""


def create_community(cookie, url):
    request = send_request(url, cookie)
    text = request.text
    pattern_community = re.compile(
        r"<strong><a href=\"forumdisplay\.php\?fid=[0-9]{1,}\">(.*)</a></strong><div class=\".*\">")
    pattern_sub_community = re.compile(
        r"class=\"subforumicon subforum_minioff ajax_mark_read\" id=\"mark_read_[0-9]{1,}\"></div><a href=\"forumdisplay\.php\?fid=[0-9]{1,}\" title=\"\">([^</a>]*)")
    communities = re.findall(pattern_community, text)
    logger.info(f"comunities which is found is: {communities} ")
    sub_communities = re.findall(pattern_sub_community, text)
    logger.info(f"sub comunities which is found is: {sub_communities} ")
    if not communities:
        raise Exception("There is no cummunity!")
    for com in communities:
        url_of_community = re.findall(f"<a href=\"(.*)\">{com}</a>", text)[0]
        try:
            new_community, status = Community.objects.get_or_create(title=com, url=url_of_community)
        except:
            logger.error(f"There is more than one community with {com} title")
            # This exception should be handel due to business logic
        logger.info(f"community is {new_community.title} ---> and the url is: {new_community.url}")
        for sub in sub_communities:
            index_of_begin = text.find(com)
            sub_text = text[index_of_begin::]
            index_of_end = text[index_of_begin::].find("</td>")
            if not Community.objects.filter(title=sub).exists() and sub_text[:index_of_end:].rfind(sub) != -1:
                url_of_sub = re.findall(f"<a href=\"([^<]*)\" title=\"\">{sub}</a>", sub_text)[0]
                try:
                    new, status = Community.objects.get_or_create(title=sub, parent=new_community, url=url_of_sub)
                except:
                    logger.error(f"There is more than one sub community with {sub} title")

                logger.info(f"community is : {new_community.title} and the sub community is :{new.title} ----> the parent of sub community is : {new.parent.title}, and url is : {new.url}")
    return "Add communities successfully"
