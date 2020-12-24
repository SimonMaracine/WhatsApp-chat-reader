import re
import sys
from datetime import datetime
from dataclasses import dataclass
from enum import Enum, auto
from collections import OrderedDict
from typing import Optional, OrderedDict as OrderedDictType

_HOUR_MAPPING = {
    0: "00:00", 1: "01:00", 2: "02:00", 3: "03:00", 4: "04:00", 5: "05:00", 6: "06:00", 7: "07:00", 8: "08:00",
    9: "09:00", 10: "10:00", 11: "11:00", 12: "12:00", 13: "13:00", 14: "14:00", 15: "15:00", 16: "16:00", 17: "17:00",
    18: "18:00", 19: "19:00", 20: "20:00", 21: "21:00", 22: "22:00", 23: "23:00"
}

_DAY_MAPPING = {
    0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"
}


class TimelineMode(Enum):
    WHOLE = auto()
    HALF = auto()
    QUARTER = auto()


class TimelinePart(Enum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()


@dataclass
class Message:
    date_time: datetime
    person_name: str
    message: str


@dataclass
class ChatData:
    people: OrderedDictType[str, int]
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

    ordered_dict = {k: v for k, v in reversed(sorted(people.items(), key=lambda item: item[1]))}
    people = OrderedDict(ordered_dict)

    return ChatData(
        people,
        len(messages),
        messages[0].date_time,
        messages[-1].date_time
    )


def get_timeline(messages: list[Message], days: int, mode: TimelineMode, part: Optional[TimelinePart] = None) \
        -> tuple[OrderedDictType[int, tuple[int, datetime]], OrderedDictType[int, str]]:  # TODO remove 'days', if not needed
    all_days: OrderedDictType[int, tuple[int, datetime]] = OrderedDict()
    dates: OrderedDictType[int, str] = OrderedDict()

    if mode is TimelineMode.WHOLE:
        start = 0
        end = len(messages)
    elif mode is TimelineMode.HALF:
        if part is TimelinePart.FIRST:
            start = 0
            end = len(messages) // 2
        elif part is TimelinePart.SECOND:
            start = len(messages) // 2
            end = len(messages)
        else:
            raise RuntimeError("Invalid timeline part")
    elif mode is TimelineMode.QUARTER:
        if part is TimelinePart.FIRST:
            start = 0
            end = len(messages) // 4
        elif part is TimelinePart.SECOND:
            start = len(messages) // 4
            end = (len(messages) // 4) * 2
        elif part is TimelinePart.THIRD:
            start = (len(messages) // 4) * 2
            end = (len(messages) // 4) * 3
        elif part is TimelinePart.FOURTH:
            start = (len(messages) // 4) * 3
            end = len(messages)
        else:
            raise RuntimeError("Invalid timeline part")
    else:
        raise RuntimeError("Invalid timeline mode")

    last_datetime = messages[0].date_time  # Take first message's datetime to begin with
    day_count = 0
    messages_this_day = 0
    first_day_in_dict = -1  # To remember the from which the graph begins

    i = 0  # Declare here, because might be referenced before assignment (maybe)
    for i, message in enumerate(messages):
        if message.date_time.day == last_datetime.day and \
                message.date_time.month == last_datetime.month and \
                message.date_time.year == last_datetime.year:
            if i == end:
                break
            messages_this_day += 1
        else:
            if start <= i:
                # Insert previous day into hash map
                all_days[day_count] = (messages_this_day, messages[i - 1].date_time)
                if first_day_in_dict == -1:
                    first_day_in_dict = day_count

                if i == end:
                    break

            # Set to 1, because this is a brand new day, so already a message
            messages_this_day = 1
            day_count += 1

            # Check for empty days
            days_passed = (message.date_time.date() - last_datetime.date()).days
            if days_passed > 1:
                for _ in range(days_passed - 1):  # Do the in-between empty days
                    if start <= i:
                        all_days[day_count] = (0, messages[i - 1].date_time)
                    day_count += 1

        last_datetime = message.date_time

    # Insert last day into hash map
    all_days[day_count] = (messages_this_day, messages[i - 1].date_time)

    # Insert first and last date
    dates[first_day_in_dict] = str(messages[start].date_time.date())
    dates[day_count] = str(messages[end - 1].date_time.date())

    all_days = OrderedDict({key: value[0] for key, value in all_days.items()})

    return all_days, dates


def get_each_day(messages: list[Message]) -> OrderedDictType[str, int]:
    days = {
        "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0
    }
    days = OrderedDict(days)

    for message in messages:
        days[_DAY_MAPPING[message.date_time.weekday()]] += 1

    return days


def get_each_hour(messages: list[Message]) -> OrderedDictType[str, int]:
    hours = {
        "00:00": 0, "01:00": 0, "02:00": 0, "03:00": 0, "04:00": 0, "05:00": 0, "06:00": 0, "07:00": 0, "08:00": 0,
        "09:00": 0, "10:00": 0, "11:00": 0, "12:00": 0, "13:00": 0, "14:00": 0, "15:00": 0, "16:00": 0, "17:00": 0,
        "18:00": 0, "19:00": 0, "20:00": 0, "21:00": 0, "22:00": 0, "23:00": 0
    }
    hours = OrderedDict(hours)

    for message in messages:
        hours[_HOUR_MAPPING[message.date_time.time().hour]] += 1

    return hours


def is_chat(file_path: str) -> bool:
    try:
        with open(file_path, "r", encoding="utf8") as file:
            first_line = file.readline()
            match = re.match("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{2} (PM|AM) - ", first_line)

            if match is not None:
                return True
            else:
                return False
    except OSError as err:
        print(err, file=sys.stderr)
        raise


def read_chat_file(file: str) -> list[Message]:
    messages = []

    try:
        with open(file, "r", encoding="utf8") as file:
            while line := file.readline():
                message = _parse_line(line, messages)
                if message is not None:
                    messages.append(message)
    except OSError as err:
        print(err, file=sys.stderr)
        raise
    except RuntimeError as err:  # Catch my own errors
        print(err, file=sys.stderr)
        raise

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
