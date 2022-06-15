import random
import sys


global guess_word
global words
global round_number


def get_try_word_results(try_word):
    if try_word == guess_word:
        print("Congradulations! {} was the word!".format(guess_word))
        sys.exit(0)

    results = ""

    for i in range(len(try_word)):
        try_word_letter = try_word[i]
        guess_word_letter = guess_word[i]

        if guess_word_letter == try_word_letter:
            results += 'G'
        elif try_word_letter in guess_word and try_word_letter != guess_word_letter:
            results += 'Y'
        else:
            results += 'N'

    return results


def start_round():
    global round_number
    round_number += 1
    valid_input = False
    while not valid_input:
        try_word = input("What word would you like to try? ")

        if try_word not in words:
            print("Invalid word: '{}'")
        else:
            valid_input = True

    round_results = get_try_word_results(try_word)

    print("Round results: {}".format(round_results))

    if round_number < 6:
        start_round()
    else:
        print("You did not find the word! It was '{}'".format(guess_word))
        sys.exit(0)


def start_game():
    global guess_word
    guess_word = words[random.randint(0, len(words) - 1)]

    start_round()


def get_all_words():
    with open('words.txt') as f:
        return [i[0:5] for i in f.readlines()]


def main():
    global words, round_number
    round_number = 0
    words = get_all_words()

    start_game()


main()
