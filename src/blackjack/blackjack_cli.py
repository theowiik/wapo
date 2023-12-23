from blackjack_core import Blackjack


def play():
    blackjack: Blackjack = Blackjack()
    blackjack.deal_cards()
    print(blackjack.display())

    while True:
        choice = input("Hit or stand? (h/s): ").lower()

        if choice == "h":
            blackjack.player_hit()
            print(blackjack.display())

            if blackjack.player_is_bust():
                break

        elif choice == "s":
            blackjack.player_stand()
            break

        else:
            print("Invalid choice. Try again.")

    print(blackjack.display())


if __name__ == "__main__":
    play()
