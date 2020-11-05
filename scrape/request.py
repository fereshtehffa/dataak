import requests


def send_request(url,  cookies):
    try:
        request = requests.get(url, cookies=cookies)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return request