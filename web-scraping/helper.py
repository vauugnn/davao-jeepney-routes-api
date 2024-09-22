import random
import requests
import re
import bs4

__all__ = ["get_request", "get_route_coords"]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
]


def get_request(url: str) -> requests.Response:
    headers = {"user-agent": random.choice(user_agents)}

    return requests.get(url, headers=headers)


def get_route_coords(url: str) -> list[tuple[str, ...]]:
    if (res := get_request(url)).status_code == 200:
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        if (entry_content := soup.select_one("article > div > div")) is not None:
            assert isinstance(entry_content, bs4.PageElement)

            iframe_all = entry_content.find_all_next("iframe")
            iframe_index = 0

            if len(iframe_all) > 1:
                while not (
                    iframe_all[iframe_index]
                    .get("src")
                    .startswith("https://www.google.com")
                ):
                    iframe_index += 1

            if (iframe := iframe_all[iframe_index]) is not None:
                assert isinstance(iframe, bs4.PageElement)

                if (res := get_request(iframe.get("src"))).status_code == 200:
                    soup = bs4.BeautifulSoup(res.text, "html.parser")

                    if (script := soup.find("script")) is not None:
                        assert isinstance(script, bs4.PageElement)

                        return re.findall(
                            r"(\[\[([\d.-]+),([\d.-]+)\]\],?)+",
                            re.findall(r'(?<=_pageData = ").*(?=")', script.text)[0],
                        )
                else:
                    raise Exception(res)
    else:
        raise Exception(res)

    return []
