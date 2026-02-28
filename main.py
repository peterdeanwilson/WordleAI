import random
from collections import Counter, defaultdict

def load_dictionary(path):
    with open(path) as f:
        return [w.strip().lower() for w in f]

def is_valid_guess(guess, guesses):
    return len(guess) == 5 and guess.isalpha() and guess in guesses

def get_pattern(guess, answer):
    pattern = ["B"] * 5
    remaining = Counter()

    # Greens first + count remaining letters in the answer
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = "G"
        else:
            remaining[answer[i]] += 1

    # Then yellows, only if that letter is still available
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
    return [w for w in candidates if get_pattern(guess, w) == pattern]

# --- "Expert" picker (entropy / expected remaining candidates) ---

def expected_remaining(guess, candidates):
    buckets = defaultdict(int)
    for ans in candidates:
        buckets[get_pattern(guess, ans)] += 1

    n = len(candidates)
    return sum(size * size for size in buckets.values()) / n  # lower = better

def pick_best_guess(candidates, guesses, sample_limit=600):
    # For speed, score only a random subset of guesses
    pool = guesses
    if len(pool) > sample_limit:
        pool = random.sample(pool, sample_limit)

    best = None
    best_score = float("inf")

    for g in pool:
        s = expected_remaining(g, candidates)
        if s < best_score:
            best_score = s
            best = g

    return best

# --- Game loop ---

def wordle(guesses, answers, use_ai=False, sample_limit=600, show_remaining=True):
    print("Welcome to Wordle! You have 6 attempts.")
    secret = random.choice(answers)

    candidates = answers[:]  # remaining possible answers

    for attempt in range(1, 7):
        if use_ai:
            guess = pick_best_guess(candidates, guesses, sample_limit=sample_limit)
            print(f"AI Guess {attempt}: {guess}")
        else:
            guess = input(f"Guess {attempt}: ").lower()

        if not is_valid_guess(guess, guesses):
            print("Invalid guess.")
            if use_ai:
                raise ValueError(f"AI produced invalid guess: {guess}")
            continue

        pattern = get_pattern(guess, secret)
        print(colour_guess(guess, pattern))

        candidates = filter_candidates(candidates, guess, pattern)
        if show_remaining:
            print(f"Possible answers left: {len(candidates)}")

        if pattern == "GGGGG":
            print("You got it!")
            return

    print("Out of guesses. The word was:", secret)

if __name__ == "__main__":
    guesses = load_dictionary("guesses.txt")
    answers = load_dictionary("answers.txt")

    # set use_ai=False to play yourself
    wordle(guesses, answers, use_ai=True, sample_limit=600, show_remaining=True)