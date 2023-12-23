from enum import Enum
import random
from typing import List, Tuple


class Suite(Enum):
    HEARTS = "HEARTS"
    DIAMONDS = "DIAMONDS"
    CLUBS = "CLUBS"
    SPADES = "SPADES"


class Card:
    """Represents a playing card with a suit and a rank."""

    def __init__(self, suit: Suite, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    """Represents a deck of playing cards."""

    def __init__(self) -> None:
        suits: list[Suite] = [Suite.HEARTS, Suite.CLUBS, Suite.DIAMONDS, Suite.SPADES]
        ranks: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self._cards: list[Card] = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self._cards)

    def draw_card(self) -> Card:
        """Draws and returns the top card from the deck."""
        return self._cards.pop()


class Blackjack:
    """Represents a game of Blackjack."""

    def __init__(self) -> None:
        self._deck: Deck = Deck()
        self.player_hand: list[Card] = []
        self.dealer_hand: list[Card] = []

    def _deal_cards(self) -> None:
        """Deals two cards each to the player and the dealer."""
        for _ in range(2):
            self.player_hand.append(self._deck.draw_card())
            self.dealer_hand.append(self._deck.draw_card())

    def _calculate_score(self, hand: List[Card]) -> int:
        """Calculates and returns the score of a hand."""
        score = 0
        ace_count = 0
        for card in hand:
            if card.rank in ["J", "Q", "K"]:
                score += 10
            elif card.rank == "A":
                ace_count += 1
                score += 11
            else:
                score += int(card.rank)

        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score

    def hit(self, hand: List[Card]) -> None:
        """Adds a card to the given hand."""
        hand.append(self._deck.draw_card())

    def stand(self) -> Tuple[str, int, int]:
        """Player decides to stand, and the dealer plays its turn."""
        return self._play_dealer_turn()

    def _is_bust(self, score: int) -> bool:
        """Returns True if the score is over 21, else False."""
        return score > 21

    def _play_dealer_turn(self) -> Tuple[str, int, int]:
        """Executes the dealer's turn after the player stands."""
        self._deal_cards()
        player_score = self._calculate_score(self.player_hand)
        dealer_score = self._calculate_score(self.dealer_hand)

        # Dealer's turn
        while dealer_score < 17:
            self.hit(self.dealer_hand)
            dealer_score = self._calculate_score(self.dealer_hand)

        if self._is_bust(dealer_score):
            return "Dealer busts", player_score, dealer_score

        if player_score > dealer_score:
            return "Player wins", player_score, dealer_score
        elif player_score < dealer_score:
            return "Dealer wins", player_score, dealer_score
        else:
            return "It's a tie", player_score, dealer_score

    def display(self) -> str:
        """Displays the current state of the game."""
        dealer_cards = ", ".join(str(card) for card in self.dealer_hand)
        player_cards = ", ".join(str(card) for card in self.player_hand)
        dealer_score = self._calculate_score(self.dealer_hand)
        player_score = self._calculate_score(self.player_hand)

        return (
            f"Dealer's Hand: [{dealer_cards}] - Score: {dealer_score}\n"
            f"Player's Hand: [{player_cards}] - Score: {player_score}\n"
        )
