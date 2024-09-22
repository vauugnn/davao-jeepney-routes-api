from src.util import *

# Run python3 web-scraping or python web-scraping from the root directory
for i in range(0, 14):
    for letter in ["", "a", "b"]:
        url = (
            "https://ph.commutetour.com/ph/routes/davao-routes/davao-jeep/route-%s-davao-city-jeep/"
            % (str(i + 1) + letter)
        )

        try:
            coords = get_route_coords(url)

            if len(coords) > 1:
                print(url)
        except BaseException as e:
            print("%s from %s" % (e, url))
