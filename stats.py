import logging
import csv
import matplotlib.pyplot as plt


def create_stats(statistics: dict, file_name: str) -> None:
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel("Time")
    plt.xlabel("Processes")
    plt.title("Stats")
    x = statistics.keys()
    y = statistics.values()
    plt.bar(x, y, color="blue", width=0.5)
    plt.savefig(file_name)
    logging.info("Create and save statistics")


def write_stats(processes: int, time: float, file_name: str) -> None:
    try:
        with open(file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([processes, time])
        logging.info("Stats successfully written")
    except OSError as err:
        logging.error("Stats writing is failed")
        raise err


def load_stats(file_name: str) -> dict:
    try:
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            stats = list(reader)
        logging.info("Stats successfully loaded")
    except OSError as err:
        logging.error("Loading stats is failed")
        raise err
    result = dict()
    for i in stats:
        processes, time = i
        result[int(processes)] = float(time)
    return result
