import sys
import json
import time
import datetime
import requests

if __name__ == "__main__":
    f = open("json.txt")
    coords = json.load(f)
    racer_1 = 0
    racer_2 = 0
    i = 0

    while racer_2 < len(coords):
        print("racer_1: {} {}".format(coords[racer_1][0],
                                      coords[racer_1][1]))
        print("racer_2: {} {}".format(coords[racer_2][0],
                                      coords[racer_2][1]))

        json = [
            {
                "position": "POINT ({} {})".format(coords[racer_1][0],
                                                   coords[racer_1][1]),
                "data": {"time": "+0:00:00"},
                "racer": 1
            },
            {
                "position": "POINT ({} {})".format(coords[racer_2][0],
                                                   coords[racer_2][1]),
                "data": {
                    "time": "-{}".format(datetime.timedelta(seconds=i * 5))},
                "racer": 2
            }
        ]

        r = requests.post(
            url="http://localhost:8000/api/v1/trackie/races/{}/data/".format(
                sys.argv[1]),
            json=json,
            auth=("admin", "root")
        )

        racer_1 += 2 if racer_1 < (len(coords) - 1) else (len(
            coords) - 1) - racer_1
        racer_2 += 1
        i += 1

        time.sleep(1)

    requests.delete(
        url="http://localhost:8000/api/v1/trackie/races/{}/data/".format(
            sys.argv[1]),
        auth=("admin", "root")
    )

sys.exit(0)
