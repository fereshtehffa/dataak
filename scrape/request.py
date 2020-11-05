import requests

from logger import Logger

logger = Logger.__call__().get_logger()


def send_request(url,  cookies):
    try:
        request = requests.get(url, cookies=cookies)

    except requests.exceptions.HTTPError as err:
        logger.error(f"There is error for get  response: {err}")
        raise SystemExit(err)
    logger.info(f"getting response from the {url} was successfully.")
    return request