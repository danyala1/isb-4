import hashlib
from tqdm import tqdm
import logging
import multiprocessing as mp


def check_hash(hash: str, card_number: str) -> bool:
    logging.info("Checking the hash")
    card_hash = hashlib.sha512(card_number.encode()).hexdigest()
    if hash == card_hash:
        return int(card_number)
    return 0


def get_card_number(
    hash: str, bins: list, last_numbs: str, core_number: int = mp.cpu_count()
) -> int:
    args = []
    for i in range(100000,1000000):
        for j in bins:
            args.append((hash, f"{j}{i}{last_numbs}"))
    with mp.Pool(processes=core_number) as p:
        for result in p.starmap(check_hash, tqdm(args, ncols=120, colour="green")):
            if result:
                p.terminate()
                logging.info("Card number got successfully")
                return result
    logging.info("Card number not got")
    return 0


def luhn(card_number: str) -> bool:
    nums = []
    card = list(map(int, card_number))
    last = card[15]
    card.pop()
    for num in card:
        tmp = num * 2
        if tmp > 9:
            nums.append(tmp % 10 + tmp // 10)
        else:
            nums.append(tmp)
    res = 0
    for num in nums:
        res += num
    res = 10 - res % 10
    logging.info("Check the card number using the Luhn algorithm")
    return res == last
