"""
Fetch publicly available gas prices from German gas stations
based on MTS-K data hosted by tankerkoenig.de.
"""

import json
from typing import Dict, Any
import requests
import pandas as pd
import sqlalchemy
from sqlalchemy.engine import Connection

class CONSTANTS(object):
    """Just a simple constant class."""

    __slots__ = ()
    with open("./parameters.jsonc", mode="r", encoding="utf8") as fopen:
        PARAMETERS = json.load(fopen)

    BASE_URL = PARAMETERS["BASE_URL"]
    API_KEY = PARAMETERS["API_KEY"]
    STATIONS = PARAMETERS["STATIONS"]
    HOST = PARAMETERS["HOST"]
    MYSQL_PORT = PARAMETERS["MYSQL_PORT"]
    MYSQL_USER = PARAMETERS["MYSQL_USER"]
    MYSQL_PASSWORD = PARAMETERS["MYSQL_PASSWORD"]


def get_mariadb_connection(
    host: str,
    user: str,
    password: str,
) -> Connection:
    """Creates a connection to a MariaDB instance.

    Args:
        host (str): Docker host
        user (str): MariaDB user
        password (str): MariaDB password

    Returns:
        conn: SQLAlchemy connection
    """
    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/fhem?charset=utf8mb4",
    )
    conn = engine.connect()

    return conn


def get_gas_stations_by_radius(
    url: str, lat: str, lng: str, rad: str, apikey: str
) -> Dict[str, Any]:
    """
    Perform API request to perform a radial search for gas stations
    around lat and lng.

    Args:
        url (str): Base url to access tankerkoenig data
        lat (str): Latitude of your reference location
        lng (str): Longitude of your reference location
        rad (str): Radius around the reference location in metres
        apikey (str): API-Key provided from tankerkoenig

    Returns:
        Dict[str, Any]: Dictionary object holding the API response.
    """

    data = {"lat": lat, "lng": lng, "rad": rad, "type": "all", "apikey": apikey}

    response = requests.get(url=url, params=data)

    response.raise_for_status()

    return json.loads(response.text)["stations"]


def main():
    """Entry point."""

    const = CONSTANTS()
    pdf: pd.DataFrame = None

    conn = get_mariadb_connection(
        host=const.HOST, user=const.MYSQL_USER, password=const.MYSQL_PASSWORD
    )

    for loc in const.STATIONS:

        data = get_gas_stations_by_radius(
            url=const.BASE_URL,
            lat=const.STATIONS[loc]["LATITUDE"],
            lng=const.STATIONS[loc]["LONGITUDE"],
            rad=const.STATIONS[loc]["RADIUS"],
            apikey=const.API_KEY,
        )

        pdf_ii = pd.DataFrame(data)
        pdf_ii["ref_loc"] = loc

        if pdf is None:
            pdf = pdf_ii
        else:
            pdf = pd.concat([pdf, pdf_ii])

    conn.execute("TRUNCATE TABLE l_t_gas_price;")

    pdf.to_sql(name="l_t_gas_price", con=conn, if_exists="append", index=False)


if __name__ == "__main__":
    main()
