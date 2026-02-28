import random
from collections import Counter

def load_dictionary(path):
    with open(path) as f:
        return [w.strip().lower() for w in f]

def is_valid_guess(guess, guesses):
    return len(guess) == 5 and guess in guesses

def evaluate_guess(guess, answer):
    colours = ["\033[0m"] * 5
    remaining = Counter()

    # mark greens and count what's left
    for i in range(5):
        if guess[i] == answer[i]:
            colours[i] = "\033[32m"
        else:
            remaining[answer[i]] += 1

    # mark yellows if possible
    for i in range(5):
        if colours[i] == "\033[32m":
            continue
        if remaining[guess[i]] > 0:
            colours[i] = "\033[33m"
            remaining[guess[i]] -= 1

    result = ""
    for i in range(5):
        result += colours[i] + guess[i]

    return result + "\033[0m"

def wordle(guesses, answers):
    print("Welcome to Wordle! You have 6 attempts.")
    secret = random.choice(answers)

    attempts = 1

    while attempts <= 6:
        guess = input(f"Guess {attempts}: ").lower()

        if not is_valid_guess(guess, guesses):
            print("Invalid guess.")
            continue

        print(evaluate_guess(guess, secret))

        if guess == secret:
            print("You got it!")
            return

        attempts += 1

    print("Out of guesses. The word was:", secret)

guesses = load_dictionary("guesses.txt")
answers = load_dictionary("answers.txt")

wordle(guesses, answers)