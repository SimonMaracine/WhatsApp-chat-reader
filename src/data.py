import re
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    date_time: datetime
    person_name: str
    message: str


@dataclass
class ChatData:
    people: dict[str, int]
    total_messages: int
    oldest_message: datetime
    newest_message: datetime


def retrieve_data(messages: list[Message]) -> ChatData:
    people = {}
    for message in messages:
        name = message.person_name
        if name not in people:
            people[name] = 0
        else:
            people[name] += 1

    return ChatData(
        people,
        len(messages),
        messages[0].date_time,
        messages[-1].date_time
    )


def is_chat(file_path: str) -> bool:
    with open(file_path, "r") as file:
        first_line = file.readline()
        match = re.match("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{2} (PM|AM) - ", first_line)

        if match is not None:
            return True
        else:
            return False


def read_chat_file(file: str) -> list[Message]:
    messages = []

    with open(file, "r") as file:
        while line := file.readline():
            message = _parse_line(line, messages)
            if message is not None:
                messages.append(message)
                print(message)

    return messages


def _parse_line(line: str, messages: list[Message]) -> Optional[Message]:
    # Check to see if this is a message line
    match = re.match("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{2} (PM|AM) - ", line)

    # If there is no match, then this line is the continuation of the last message
    if match is None:
        messages[-1].message += "\n" + line.rstrip("\n")
        return None

    hypen_pos = line.find(" - ")
    if hypen_pos == -1:
        raise RuntimeError("Chat file is corrupted")

    message_info_str = line[0:hypen_pos]
    message_info: list = message_info_str.split(" ")
    date: str = message_info[0].rstrip(",")
    time: str = message_info[1]
    meridian: str = message_info[2]

    month, day, year = list(map(int, date.split("/")))
    year += 2000
    hour, minute = _parse_12_format_time(time, meridian)

    date_time = datetime(year, month, day, hour, minute)

    person_and_message: str = line[hypen_pos + 3:]
    delimiter = person_and_message.find(": ")

    # If there is no delimeter, then this line is not a message, so skip it
    if delimiter == -1:
        return None

    person_name = person_and_message[0:delimiter]
    message = person_and_message[delimiter + 2:].rstrip("\n")

    return Message(date_time, person_name, message)


def _parse_12_format_time(time: str, meridian: str) -> tuple[int, int]:
    colon_pos = time.find(":")
    if colon_pos == -1:
        raise RuntimeError("Chat file is corrupted")

    try:
        hour12 = int(time[0:colon_pos])
        minute12 = int(time[colon_pos + 1:])
    except ValueError:
        raise RuntimeError("Chat file is corrupted")

    if meridian == "AM":
        if hour12 == 12:
            hour24 = hour12 - 12
        else:
            hour24 = hour12
    elif meridian == "PM":
        if 11 >= hour12 >= 1:
            hour24 = hour12 + 12
        else:
            hour24 = hour12
    else:
        raise RuntimeError("Chat file is corrupted")

    return hour24, minute12
