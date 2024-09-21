import re
from bs4 import BeautifulSoup, Tag
from helper import get_request

if (
    res := get_request(
        "https://ph.commutetour.com/ph/routes/davao-routes/davao-jeep/route-2-davao-city-jeep/"
    )
).status_code == 200:
    soup = BeautifulSoup(res.text, "html.parser")

    if (div := soup.find("div", attrs={"id": "route"})) is not None:
        if (iframe := div.find("iframe")) is not None:
            assert isinstance(iframe, Tag)
            res = get_request(iframe.get("src"))

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")

                script = soup.find("script")
                assert isinstance(script, Tag)

                # TODO: Extract coordinates from _pageData variable.
                print(re.findall(r'(?<=_pageData = ").*(?=")', script.text)[0])
            else:
                print(res)
else:
    print(res)
