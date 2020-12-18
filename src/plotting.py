import matplotlib.pyplot as plt

from data import Message, get_timeline, get_each_day, get_each_hour


def timeline(messages: list[Message], is_bar: bool):
    timeline_ = get_timeline(messages)
    days = list(timeline_.keys())
    messages_count = list(timeline_.values())

    plt.figure(figsize=(9, 5))

    if is_bar:
        plt.bar(days, messages_count)
    else:
        plt.plot(days, messages_count)

    plt.gca().xaxis.get_major_locator().set_params(integer=True)
    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    plt.xlabel("Day Count")
    plt.ylabel("No. Messages")
    plt.title("Timeline")
    plt.grid()

    plt.show()


def week(messages: list[Message]):
    each_day = get_each_day(messages)
    days = list(each_day.keys())
    messages_count = list(each_day.values())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(days, messages_count)

    plt.xlabel("Day")
    plt.ylabel("No. Messages")
    plt.title("Week")
    plt.grid()

    plt.show()


def day(messages: list[Message]):
    each_hour = get_each_hour(messages)
    hours = list(each_hour.keys())
    messages_count = list(each_hour.values())

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.bar(hours, messages_count)

    plt.xlabel("Hour")
    plt.ylabel("No. Messages")
    plt.title("Day")
    plt.grid()

    plt.show()
