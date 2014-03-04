# Jessica Rex
# Guess my number (revised for Chapter 6 challenge)
#
# The computer picks a random number between 1 and 100
# The player tries to guess it and the computer lets
# the player know if the guess is too high, too low
# or right on the money.
#
# This uses functions and parameters to run.

import random

def ask_number(question, low, high, step = 1):
    """Ask for a number within a range."""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

def main():
    print("\tWelcome to 'Guess My Number'!")
    print("\nI'm thinking of a number between 1 and 100.")
    print("Try to guess it in as few attempts as possible.\n")

    # set the initial values
    the_number = random.randint(1, 100)
    guess = ask_number("Take a guess: ", 0, 100)
    tries = 1

    # guessing loop
    while guess != the_number:
        if guess > the_number:
            print("lower...")
        else:
            print("higher...")

        guess = int(input("Take a guess: "))
        tries += 1

    print("You guessed it! The number was", the_number)
    print("And it only took you", tries, "tries!\n")

# run the program
main()
input("\n\nPress the enter key to exit.")
