import random
import sys

CHECKED_LETTERS = []
CONFIRMED_LETTERS = []
ROUND_NUMBER = 1


# Method for printing words
def print_words(words):
    words = sorted(words)
    for i in range(len(words)):
        print("{}. {}".format(i + 1, words[i]))
    print("\n")


# Method for asking and getting a random word from the potential words list
def get_random_word(words):
    try_word = words[random.randint(0, len(words) - 1)]
    print("Try '{}'".format(try_word))

    return try_word


# Method for asking which custom word you would like to try
def get_custom_word(words):
    try_word = ""
    while len(try_word) != 5:
        try_word = input("What word would you like to try? ")
        if len(try_word) != 5:
            print("Word must be a length of 5")
        elif not try_word.isalpha():
            print("Only letter characters are allowed")
            try_word = ""
        elif try_word not in words:
            print("Word not found in list of potential words...")
            user_input = input(
                "Do you want to see a list of potential words? (y/n)")

            if user_input == 'y':
                print_words(words)

            try_word = ""

    return try_word


# Method for taking in the results from the try_word being inputted and outputting a list of potential words
# The results string should be in the format of (g*y*n*)
def analyze_results(results, words, try_word):
    global ROUND_NUMBER
    current_char_index = 0
    for results_letter in results:
        results_letter = results_letter.lower()
        current_letter = try_word[current_char_index]

        if results_letter == 'g':
            CONFIRMED_LETTERS.append(current_letter)
            g_list = []
            for word in words:
                # Filters out any words that don't have that specific letter at the proper index
                if current_letter == word[current_char_index]:
                    g_list.append(word)
            words = g_list

        elif results_letter == 'y':
            CHECKED_LETTERS.append(current_letter)
            y_list = []
            for word in words:
                # Filters out any words that don't have the letter in it and words that have the letter at that specific position
                if current_letter in word and current_letter != word[current_char_index]:
                    y_list.append(word)
            words = y_list

        elif results_letter == 'n':
            n_list = []
            if len(words) < 3:
                break
            for word in words:
                if current_letter not in word:
                    if ROUND_NUMBER == 1:
                        n_list.append(word)
                    elif len(CHECKED_LETTERS) == 0:
                        n_list.append(word)
                    else:
                        if current_letter != word[current_char_index]:
                            n_list.append(word)
            words = n_list

        current_char_index += 1

    if try_word in words:
        words.remove(try_word)

    return words


# Gets the results from the user from trying the word in Wordle
def get_results():
    results = ""
    while len(results) != 5:
        results = input(
            "What results did you get from that? ((G)reen, (Y)ellow, (N)o Match): ")

        if len(results) != 5:
            print(
                "Please enter a string of length 5 consisting of G/Y/N based on the results from the wordle!")

        for letter in results:
            if letter.lower() not in ['y', 'n', 'g']:
                print("Invalid character - {}".format(letter))
                results = ""

    if results.lower() == 'ggggg':
        print("Congratulations!")
        sys.exit(0)

    return results


# Main method for the game, run when trying a new round.
def solve(words):
    global ROUND_NUMBER
    try_word_option = input("Options:\n\t{}\n\t{}\n".format(
        "(1). Try random word", "(2). Try custom word"))
    try_word = ""
    if try_word_option == '1':
        try_word = get_random_word(words)

    elif try_word_option == '2':
        try_word = get_custom_word(words)
    else:
        print("Invalid Answer - Trying random word...")
        try_word = get_random_word(words)

    words = analyze_results(get_results(), words, try_word)

    if ROUND_NUMBER > 6:
        print("Unfortunately you did not get it in time :(")
        sys.exit(0)

    print_bool = input("Print valid matches? (y/n) ")
    if print_bool != 'n':
        print_words(words)

    ROUND_NUMBER += 1
    solve(words)


def get_all_words():
    with open('words.txt') as f:
        return [i[0:5] for i in f.readlines()]


def main():
    all_words = get_all_words()
    debug = False
    try:
        solve(sorted(all_words))
    except Exception as e:
        if debug:
            print(e)
        else:
            print("Word not found, try again!")


main()
