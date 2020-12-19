import matplotlib.pyplot as plt

from data import Message, get_timeline, get_each_day, get_each_hour


def timeline(messages: list[Message], is_bar: bool, days: int):
    all_days, dates = get_timeline(messages, days)
    days = list(all_days.keys())
    messages_count = list(all_days.values())

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    if is_bar:
        ax1.bar(days, messages_count)
    else:
        ax1.plot(days, messages_count)

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(list(dates.keys()))
    ax2.set_xticklabels(list(dates.values()))

    ax1.xaxis.get_major_locator().set_params(integer=True)
    ax1.yaxis.get_major_locator().set_params(integer=True)

    ax1.set_xlabel("Day Count")
    ax1.set_ylabel("No. Messages")
    ax1.grid()
    plt.title("Timeline")

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

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.bar(hours, messages_count)

    plt.xlabel("Hour")
    plt.ylabel("No. Messages")
    plt.title("Day")
    plt.grid()

    plt.show()
