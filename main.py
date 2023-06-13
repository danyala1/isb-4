import logging
import argparse
import time
import load_write
from card import get_card_number, luhn
import stats


def card_number(settings: dict) -> None:
    """Searches for the card number
    
    Args: dict - statictic

    """
    try:
        hash = settings["hash"]
        bins = settings["bins"]
        last_numbers = settings["last_numbers"]
        card_number = get_card_number(
            hash, bins, last_numbers, args.get_card_numb)
        if card_number:
            load_write.write_file(
                str(card_number), settings["card_number"])
            logging.info("Card number found")
        else:
            logging.info("Card number not found")
    except BaseException as err:
        logging.error(f"Something went wrong: {err}")

def luhn_algorithm(settings: dict) -> None:
    """Checks for the Luhn's algorithm
    
    Args: dict - statictic
    
    """
    card_number = load_write.read_file(settings["card_number"])
    if luhn(card_number):
        load_write.write_file(
            " Luhn algorithm: true", settings["card_number"])
        logging.info("Card number is right")
    else:
        load_write.write_file(
            " Luhn algorithm: false", settings["card_number"])
        logging.info("Card number is wrong")

def statistics(settings: dict) -> None:
    """Makes statistics

    Args: dict - statictiс

    """
    try:
        hash = settings["hash"]
        bins = settings["bins"]
        last_four_numbers = settings["last_numbers"]
        for i in range(1, 9):
            t1 = time.time()
            get_card_number(hash, bins, last_four_numbers, i)
            t2 = time.time()
            stats.write_stats(i, t2 - t1, settings["stats"])
        stats.create_stats(stats.load_stats(
            settings["stats"]), settings["graph"])
        logging.info("Stats got and saved successfully")
    except BaseException:
        logging.error("Something went wrong")

if __name__ == "__main__":
    logging.basicConfig(level = logging.ERROR,
                        filename="prog_logs.log", filemode="w")
    settings = load_write.load_settings("settings.json")
    parser = argparse.ArgumentParser()
    parser.add_argument("-card", "--get_card_numb", type=int,
                        help="Gets card number, input the number of processors")
    parser.add_argument("-luhn", "--luhn_algorithm",
                        help="Checking the card number using the Luhn algorithm")
    parser.add_argument("-stat", "--statistics",
                        help="Gets stats about executing time with different number of processors")
    args = parser.parse_args()
    if args.get_card_numb:
        card_number(settings)
    elif args.luhn_algorithm:
        luhn_algorithm(settings)
    elif args.statistics:
        statistics(settings)
