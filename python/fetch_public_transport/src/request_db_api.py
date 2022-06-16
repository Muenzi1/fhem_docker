"""Script to web scrape DB departure data, create FHEM devices, update their
data and create a new ReadingsGroup object as visual."""

import json
from fhem import Fhem

import dep_lib.dep_lib as dl


class CONSTANTS(object):
    __slots__ = ()
    with open("./parameters.jsonc", mode="r", encoding="utf8") as fopen:
        PARAMETERS = json.load(fopen)

    NUMBER_CONNECTIONS = PARAMETERS["NUMBER_CONNECTIONS"]
    PRODUCTS = PARAMETERS["PRODUCTS"]
    BASE_URL = PARAMETERS["BASE_URL"]
    STATIONS = PARAMETERS["STATIONS"]
    DEPARTURE_DEVICE = PARAMETERS["DEVICE"]
    HOST = PARAMETERS["HOST"]
    FHEM_PORT = PARAMETERS["FHEM_PORT"]
    CSRF_TOKEN = PARAMETERS["CSRF_TOKEN"]
    HOST = "raspberrypi3"


def main():
    """Entry point."""

    const = CONSTANTS()

    fhem_session = Fhem(
        const.HOST, protocol="http", port=const.FHEM_PORT, csrf=const.CSRF_TOKEN
    )

    for station in const.STATIONS.values():

        station_id = station["ID"]
        device_reading = station["READING"]
        device_name = f"{const.DEPARTURE_DEVICE}_{device_reading.lower()}"

        dl.create_device(
            fh=fhem_session, device_name=device_name, if_exists="skip"
        )

        departures = dl.get_departures(
            base_url=const.BASE_URL,
            products=const.BASE_URL,
            station_id=station_id,
            num_connections=const.NUMBER_CONNECTIONS,
        )

        fhem_session.get(device_reading)

        dl.create_or_update_attr_list(
            data=departures, device_name=device_name, fh=fhem_session
        )
        dl.update_reading_list(
            fh=fhem_session,
            data=departures,
            device_name=device_name,
        )


        # create_readingsGroup(data=departures, fh=fhem_session)


if __name__ == "__main__":
    main()
