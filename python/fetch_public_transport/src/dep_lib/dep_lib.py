import datetime as dt
import itertools
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from fhem import Fhem


def create_device(
    fh: Fhem, device_name: str, if_exists: str = "skip"
) -> None:
    """Creates the FHEM device. If if_exists is set to skip, an existing devices are skipped.

    Args:
        fh (Fhem): FHEM session
        device_name (str): Name of the FHEM device to be created
        if_exists (str, optional): Controls what happens for existing devices. Either "skip" if
            existing devices should be skipped, otherwise replace. Defaults to "skip".
    """

    is_existing_device = bool(fh.get_device(device=device_name))

    if not is_existing_device:
        # Create not existing devices
        fh.send_cmd(f"define {device_name} dummy")
    elif (is_existing_device) & (if_exists == "replace"):
        # First delete the device
        fh.send_cmd(f"delete {device_name}")

        # Recreate the device
        fh.send_cmd(f"define {device_name} dummy")
    elif (is_existing_device) & (if_exists == "skip"):
        # Don't do anything as device exists and should be skipped.
        pass


def get_departures(
    base_url: str, products: str, num_connections: int, station_id: str
) -> dict:
    """_summary_

    Args:
        base_url (str): Base url to request the DB Reiseauskunft
        num_connections (int): Number of connections to fetch.
        products (str): Product string defining which DB products should be collected. Need
            to be collected by a sample request using the Reiseauskunft portal.
        station_id (str): ID of the departure station. Needs to be checked by a sample
            request using the Reiseauskunft portal.

    Returns:
        dict: Dictionary holding the parsed connection information.
    """

    con_type = "dep"  # dep for departure, arr for arrival

    url = (
        f"{base_url}?si={station_id}&bt={con_type}&p={products}&max={num_connections}"
        "&rt=1&use_realtime_filter=1&start=yes"
    )

    response = requests.get(url)

    css_soup = BeautifulSoup(response.content, "html.parser")

    dict_connection = {}

    for dd, dep in enumerate(css_soup.find_all(True, {"class": ["sqdetailsDep trow"]})):
        str_red = " ".join([entry.text for entry in dep.find_all(class_="red")])

        list_bold = dep.find_all(class_="bold")
        list_delay_on_time = dep.find_all(class_="delayOnTime")

        list_dest = [
            re.findall(r"\n>>\n([\w|\s|\(|\)|,|\-)]+)\n", item)
            for item in dep.contents
            if isinstance(item, NavigableString)
        ]

        destination = "".join(list(itertools.chain.from_iterable(list_dest)))
        list_track = [
            re.findall(r"\xa0\xa0([\w|\s|,|.)]+)", item)
            for item in dep.contents
            if isinstance(item, NavigableString)
        ]

        track = "".join(list(itertools.chain.from_iterable(list_track)))

        train = list_bold[0].text
        train = re.sub(r"[\s]{1,4}", " ", train)  # removes multiple whitespaces

        dep_time = dt.datetime.strptime(list_bold[1].text, "%H:%M")
        delay_time = list_delay_on_time[0].text if len(list_delay_on_time) > 0 else None

        if delay_time:
            delay_mins = int(
                (dt.datetime.strptime(delay_time, "%H:%M") - dep_time).seconds / 60
            )
        else:
            delay_mins = 0

        dict_connection[dd] = {
            "destination": destination,
            "track": track,
            "train": train,
            "departure": dep_time.strftime("%H:%M"),
            "delay": delay_mins,
            "info": str_red,
            "con_list": [
                train,
                destination,
                track,
                dep_time.strftime("%H:%M"),
                delay_mins,
            ],
        }

    dict_connection["type"] = con_type

    return dict_connection


def get_readings(data: dict) -> dict:
    """Returns data from data dictionary."""

    readings = {}
    con_type = data.get("type")

    for con_num, con in data.items():
        if con_num == "type":
            continue

        for key, value in con.items():
            name = f"{con_type}_{con_num}_{key}"
            readings[name] = value

    return readings


def update_reading_list(fh: Fhem, device_name: str, data: dict) -> None:
    """Updates the reading list
        fh (Fhem): FHEM session
        device_name (str): Name of the FHEM device to be created
    Args:
        fh (Fhem): FHEM session
        target_device_name (str): FHEM device to write to.
        data (dict): Dictionary holding all the connection data
    """

    con_list = []

    readings = get_readings(data)

    for reading, value in readings.items():
        if not reading.endswith("_con_list"):
            value = value if not value == "" else None
            command = f"setreading {device_name} {reading} {value}"
            fhem_msg = fh.send_cmd(command)
            if fhem_msg != b"":
                print(fhem_msg)

        else:
            con_list.append(value)

    command = f"setreading {device_name} as_array {con_list}".replace("'", '"')
    fhem_msg = fh.send_cmd(command)
    if fhem_msg != b"":
        print(fhem_msg)


def get_attr_list(data: dict) -> str:
    """Returns attribute list from data dictionary."""

    attr_list = []
    con_type = data.get("type")

    for con_num, con in data.items():
        if con_num == "type":
            continue

        for key, _ in con.items():
            attr_name = f"{con_type}_{con_num}_{key}"
            attr_list.append(attr_name)

    attr_string = ", ".join(attr_list)

    return attr_string


def create_or_update_attr_list(fh: Fhem, device_name: str, data: dict) -> None:
    """Updates DEPARTURE_DEVICE readingList attribute."""

    attribute = "readingList"
    is_existing_attr = bool(fh.get_device_attribute(device_name, attribute))

    attr_string = get_attr_list(data=data)

    if is_existing_attr:
        print("Attribute exists. Skip step.")
        return

    # Create not existing devices
    command = f"attr {device_name} readingList {attr_string}"
    fhem_msg = fh.send_cmd(command)
    if fhem_msg != b"":
        print(fhem_msg)


def create_readingsgroup(fh: Fhem, device: str, data: dict) -> None:
    """Create the FHEM ReadingsGroup device as table visual."""

    command_header = (
        "define rg_departure readingsGroup "
        "<ID>,<Gl.>,<Richtung>,<Abfahrt>,<Delay>,<Info> \n"
    )
    command_row = []

    con_type = data.get("type")

    for con_num, con in data.items():
        if con_num == "type":
            continue

        attr_list = []
        for key, _ in con.items():
            attr_name = f"{con_type}_{con_num}_{key}"
            attr_list.append(attr_name)

        attr_list = (
            attr_list[2],
            attr_list[1],
            attr_list[0],
            attr_list[3],
            attr_list[4],
            attr_list[5],
        )

        attr_list = f"{device}:{','.join(attr_list)}"
        command_row.append(attr_list)

    command = command_header + r" \ \n".join(command_row)

    fhem_msg = fh.send_cmd(command)
    if fhem_msg != b"":
        print(fhem_msg)
