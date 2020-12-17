import matplotlib.pyplot as plt

from data import Message, get_each_day


def timeline(messages: list[Message]):
    each_day = get_each_day(messages)
    days = list(each_day.keys())
    messages_count = list(each_day.values())

    plt.plot(days, messages_count)

    plt.xlabel("Day Count")
    plt.ylabel("No. Messages")
    plt.title("Timeline")
    plt.show()
