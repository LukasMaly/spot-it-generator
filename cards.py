from itertools import *
import math


def is_prime(n):
    """
    Check if number is a prime.

    :param n: number to be checked
    """
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


def create_cards(p):
    """
    Creates the list of sets with images' numbers.

    :param p: order of the game
    """
    if not is_prime(p):
        raise ValueError("The order must be a prime number.")
    for min_factor in range(2, 1 + int(p ** 0.5)):
        if p % min_factor == 0:
            break
    else:
        min_factor = p
    cards = []
    for i in range(p):
        cards.append(set([i * p + j for j in range(p)] + [p * p]))
    for i in range(min_factor):
        for j in range(p):
            cards.append(set([k * p + (j + i * k) % p
                              for k in range(p)] + [p * p + 1 + i]))

    cards.append(set([p * p + i for i in range(min_factor + 1)]))
    return cards, p * p + p + 1


def display_using_stars(cards, num_pictures):
    for pictures_for_card in cards:
        print("".join('*' if picture in pictures_for_card else ' '
                      for picture in range(num_pictures)))


def display_using_numbers(cards):
    for pictures_for_card in cards:
        print(pictures_for_card)


def check_cards(cards):
    for card, other_card in combinations(cards, 2):
        if len(card & other_card) != 1:
            print("Cards", sorted(card), "and", sorted(other_card),
                  "have intersection", sorted(card & other_card))


if __name__ == '__main__':
    order = 7
    cards, num_pictures = create_cards(order)
    display_using_stars(cards, num_pictures)
    display_using_numbers(cards)
    check_cards(cards)
