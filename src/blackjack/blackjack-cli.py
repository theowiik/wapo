from blackjack import Blackjack


def play():
    blackjack: Blackjack = Blackjack()
    blackjack.deal_cards()
    print(blackjack.display())

    while True:
        choice = input("Hit or stand? (h/s): ").lower()

        if choice == "h":
            blackjack.hit()
            print(blackjack.display())

            if blackjack.is_bust():
                print("You bust!")
                break

        elif choice == "s":
            result = blackjack.stand()
            print(f"{result[0]}! Your score: {result[1]}. Dealer score: {result[2]}.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    play()
