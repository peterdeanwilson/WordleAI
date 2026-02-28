import random
from collections import Counter

def load_dictionary(path):
    with open(path) as f:
        return [w.strip().lower() for w in f]

def is_valid_guess(guess, guesses):
    return len(guess) == 5 and guess in guesses

def get_pattern(guess, answer):
    # returns a 5-char string like "GYBBY" (duplicate-safe)
    pattern = ["B"] * 5
    remaining = Counter()

    # greens first, and count what's left in the answer
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = "G"
        else:
            remaining[answer[i]] += 1

    # then yellows if that letter is still available
    for i in range(5):
        if pattern[i] == "G":
            continue
        ch = guess[i]
        if remaining[ch] > 0:
            pattern[i] = "Y"
            remaining[ch] -= 1

    return "".join(pattern)

def colour_guess(guess, pattern):
    out = ""
    for i, ch in enumerate(guess):
        if pattern[i] == "G":
            out += "\033[32m" + ch
        elif pattern[i] == "Y":
            out += "\033[33m" + ch
        else:
            out += "\033[0m" + ch
    return out + "\033[0m"

def filter_candidates(candidates, guess, pattern):
    # keep only words that would produce the same pattern
    return [w for w in candidates if get_pattern(guess, w) == pattern]

def wordle(guesses, answers):
    print("Welcome to Wordle! You have 6 attempts.")
    secret = random.choice(answers)

    candidates = answers[:]  # <- Step 2: start with all possible answers

    for attempt in range(1, 7):
        guess = input(f"Guess {attempt}: ").lower()

        if not is_valid_guess(guess, guesses):
            print("Invalid guess.")
            continue

        pattern = get_pattern(guess, secret)          # <- Step 1
        print(colour_guess(guess, pattern))

        # update candidate list based on what we learned
        candidates = filter_candidates(candidates, guess, pattern)   # <- Step 2
        print(f"Possible answers left: {len(candidates)}")

        if pattern == "GGGGG":
            print("You got it!")
            return

    print("Out of guesses. The word was:", secret)

guesses = load_dictionary("guesses.txt")
answers = load_dictionary("answers.txt")

wordle(guesses, answers)