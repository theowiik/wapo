import sys

sys.path.append("..")
from src.blackjack.blackjack import Blackjack


def play():
    blackjack: Blackjack = Blackjack()
    blackjack.deal_cards()
    print(blackjack.display())
    print("\n\n\n")

    while True:
        choice = input("Hit or stand? (h/s): ").lower()

        if choice == "h":
            blackjack.hit()
            print(blackjack.display())
            print("\n\n\n")

            if blackjack.is_bust():
                break

        elif choice == "s":
            blackjack.stand()
            break

        else:
            print("Invalid choice. Try again.")

    print(blackjack.display())
    print("\n\n\n")


if __name__ == "__main__":
    play()
