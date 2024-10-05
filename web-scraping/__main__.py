import sqlite3
import json
from functools import reduce
from src.util import *


# PLEASE run this script from the root directory.
with sqlite3.connect(get_db_path("routes.sqlite")) as conn:
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Routes (
            id TEXT PRIMARY KEY,
            coordinates TEXT NOT NULL
        );
        """
    )

    # [(id, coordinates)]
    routes_to_insert: list[tuple[str, str]] = []

    for i in range(0, 14):
        for letter in ["", "a", "b"]:
            route_id = f"{i + 1}{letter}"
            route_url = (
                "https://ph.commutetour.com/ph/routes/davao-routes/davao-jeep/route-%s-davao-city-jeep/"
                % route_id
            )

            try:
                route_coords = get_route_coords(route_url)
            except Exception as e:
                print(f"Error {e} from {route_url}")
                continue

            routes_to_insert.append((route_id, json.dumps(route_coords)))

    cursor.executemany(
        """
        INSERT INTO Routes (id, coordinates)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE
            SET coordinates = excluded.coordinates;
        """,
        routes_to_insert,
    )

    conn.commit()

    print(
        f"Routes \"{reduce(lambda acc, v: f'{acc}{', ' if (len(acc) > 0) else ''}{str(v[0])}', routes_to_insert, '')}\" inserted/updated successfully."
    )

    cursor.close()
