import os
import sys

sys.path.append("..")

from src.blackjack.blackjack import Blackjack


def clear():
    os.system("cls||clear")


def play():
    blackjack: Blackjack = Blackjack()
    blackjack.deal_cards()
    clear()
    print(blackjack.display())

    while True:
        choice = input("Hit or stand? (h/s): ").lower()

        if choice == "h":
            blackjack.hit()
            clear()
            print(blackjack.display())

            if blackjack.is_bust():
                break

        elif choice == "s":
            blackjack.stand()
            break

        else:
            print("Invalid choice. Try again.")

    clear()
    print(blackjack.display())


if __name__ == "__main__":
    play()
