import random
from collections import Counter


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
        guess = input(prompt).strip()
        if not valid or guess in valid:
            break
    return guess


def inform(format_string, bulls, cows):
    print(format_string.format(bulls, cows))

