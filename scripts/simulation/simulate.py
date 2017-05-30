import os
import sys
import json
import time
import datetime
import requests

if __name__ == "__main__":
    file_path = os.path.abspath(__file__)
    current_path = os.path.dirname(file_path)
    json_path = os.path.join(current_path, "json.txt")
    f = open(json_path)
    coords = json.load(f)
    racer_1 = 0
    racer_2 = 0
    i = 0

    while racer_2 < len(coords):
        json = [
            {
                "position": "POINT ({} {})".format(coords[racer_1][0],
                                                   coords[racer_1][1]),
                "data": {
                    "time": "{}".format(datetime.timedelta(seconds=racer_1)),
                    "team": "Lazy",
                },
                "racer": 1
            },
            {
                "position": "POINT ({} {})".format(coords[racer_2][0],
                                                   coords[racer_2][1]),
                "data": {
                    "time": "{}".format(datetime.timedelta(seconds=i * 2)),
                    "team": "Barracuda",
                },
                "racer": 2
            }
        ]

        r = requests.post(
            url="http://localhost:8000/api/v1/trackie/races/{}/data/".format(
                sys.argv[1]),
            json=json,
            auth=("admin", "admin")
        )

        print(r.status_code, r.request.url)

        r.raise_for_status()

        racer_1 += 2 if racer_1 < (len(coords) - 1) else (len(
            coords) - 1) - racer_1
        racer_2 += 1
        i += 1

        time.sleep(1)

    requests.delete(
        url="http://{}/api/v1/trackie/races/{}/data/".format(
            sys.argv[2], sys.argv[1]),
        auth=("admin", "admin")
    )

sys.exit(0)
