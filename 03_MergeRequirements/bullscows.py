import random
import sys
import os
import cowsay
from urllib import request
from collections import Counter


def string_by_cow(s):
    cow = random.choice(cowsay.list_cows())
    return cowsay.cowsay(s, cow=cow)


def bullscows(guess, secret):
    bulls = sum(x == y for x, y in zip(guess, secret))
    cows = sum((Counter(guess) & Counter(secret)).values())
    return bulls, cows


def gameplay(ask, inform, words):
    secret = random.choice(words)

    count = 0
    while True:
        guess = ask("Введите слово: ", words)
        count += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)

        if guess == secret:
            break

    print(count)


def ask(prompt, valid=None):
    while True:
        guess = input(string_by_cow(prompt) + '\n').strip()
        if not valid or guess in valid:
            break
    return guess


def inform(format_string, bulls, cows):
    print(string_by_cow(format_string.format(bulls, cows)))


def main():
    if len(sys.argv) not in {2, 3}:
        raise SyntaxError("Wrong format of args")

    dct_address = sys.argv[1]
    file = None
    if os.path.exists(dct_address):
        file = open(dct_address, "r")
    else:
        file = [word.decode() for word in request.urlopen(dct_address)]
        if not file:
            raise ValueError("No such file")

    words_len = 5
    if len(sys.argv) == 3:
        try:
            words_len = int(sys.argv[2])
        except ValueError:
            raise ValueError("Wrong format of length of words")

    dct = [
        stripped_word
        for word in file
        if len(stripped_word := word.strip()) == words_len
    ]

    gameplay(ask, inform, dct)


if __name__ == "__main__":
    main()