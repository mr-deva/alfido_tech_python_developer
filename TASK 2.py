import random
import logging
from datetime import datetime

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="guess_game.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Game Class
# -----------------------------
class NumberGuessingGame:
    def __init__(self, lower=1, upper=100):
        self.lower = lower
        self.upper = upper
        self.secret_number = random.randint(lower, upper)
        self.attempts = 0
        logging.info("A new game has started with range %d to %d", lower, upper)

    def get_user_guess(self):
        """Safely get a guess from user"""
        while True:
            try:
                guess = int(input(f"Enter your guess ({self.lower}-{self.upper}): "))
                if self.lower <= guess <= self.upper:
                    return guess
                else:
                    print(f"⚠ Please enter a number between {self.lower} and {self.upper}.")
            except ValueError:
                print("⚠ Invalid input! Please enter a valid integer.")

    def check_guess(self, guess):
        """Compare user guess with the secret number"""
        self.attempts += 1

        if guess < self.secret_number:
            return "🔽 Too Low!"
        elif guess > self.secret_number:
            return "🔼 Too High!"
        else:
            return "🎉 Correct!"

    def play(self):
        """Main game loop"""
        print("\n🔢 Welcome to the Number Guessing Game!")
        print(f"Guess the number between {self.lower} and {self.upper}.\n")

        while True:
            guess = self.get_user_guess()
            result = self.check_guess(guess)
            print(result)

            if result == "🎉 Correct!":
                logging.info("User guessed the number %d in %d attempts",
                            self.secret_number, self.attempts)
                print(f"🏆 You guessed it in {self.attempts} attempts!\n")
                break


# -----------------------------
# Play Again Function
# -----------------------------
def ask_replay():
    """Ask the user if they want to play again"""
    while True:
        choice = input("Do you want to play again? (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            return choice
        print("⚠ Please enter 'y' or 'n'.")


# -----------------------------
# Program Entry Point
# -----------------------------
if __name__ == "__main__":
    print("=== Number Guessing Game (Advanced Version) ===")

    while True:
        game = NumberGuessingGame(1, 100)
        game.play()

        if ask_replay() == 'n':
            print("\n👋 Thanks for playing! Goodbye.")
            logging.info("Game session ended by user.")
            break

        print("\n🔁 Starting a new game...\n")
