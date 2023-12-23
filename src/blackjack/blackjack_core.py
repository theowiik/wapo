from enum import Enum
import random
from typing import List
from prettytable import PrettyTable


class Suite(Enum):
    HEARTS = "HEARTS"
    DIAMONDS = "DIAMONDS"
    CLUBS = "CLUBS"
    SPADES = "SPADES"


class Card:
    """Represents a playing card with a suit and a rank."""

    RANKS: list[str] = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
        "A",
    ]

    def __init__(self, suit: Suite, rank: str) -> None:
        if suit not in [Suite.HEARTS, Suite.DIAMONDS, Suite.CLUBS, Suite.SPADES]:
            raise ValueError("Invalid suit")

        if rank not in self.RANKS:
            raise ValueError("Invalid rank")

        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit.value.title()}"


class Deck:
    """Represents a deck of playing cards."""

    def __init__(self) -> None:
        suits: list[Suite] = [Suite.HEARTS, Suite.CLUBS, Suite.DIAMONDS, Suite.SPADES]
        self._cards: list[Card] = [
            Card(suit, rank) for suit in suits for rank in Card.RANKS
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self._cards)

    def draw_card(self) -> Card:
        """Draws and returns the top card from the deck."""
        return self._cards.pop()


class InvalidMove(Exception):
    pass


class GameState(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PLAYER_WON = "PLAYER_WON"
    DEALER_WON = "DEALER_WON"
    DRAW = "DRAW"


class Blackjack:
    """Represents a game of Blackjack."""

    _has_dealt_cards: bool = False
    _game_state: GameState = GameState.IN_PROGRESS

    def __init__(self) -> None:
        self._deck: Deck = Deck()
        self.player_hand: list[Card] = []
        self.dealer_hand: list[Card] = []

    def deal_cards(self) -> None:
        """Deals two cards each to the player and the dealer."""
        if self._has_dealt_cards:
            raise InvalidMove("Cards have already been dealt")

        if self._game_state != GameState.IN_PROGRESS:
            raise InvalidMove("Game has already finished")

        self._has_dealt_cards = True

        for _ in range(2):
            self.player_hand.append(self._deck.draw_card())
            self.dealer_hand.append(self._deck.draw_card())

    def player_stand(self) -> None:
        """Player decides to stand, finishing their turn and the dealer plays its turn."""

        if not self._has_dealt_cards:
            raise RuntimeError("Game has not started, initial cards needs to be dealt")

        if self._game_state != GameState.IN_PROGRESS:
            raise InvalidMove("Game has already finished")

        self._play_dealer_turn()

    def display(self) -> str:
        """Gets a string representing the current state of the game."""
        dealer_cards = ", ".join(str(card).split(" ")[0] for card in self.dealer_hand)
        player_cards = ", ".join(str(card).split(" ")[0] for card in self.player_hand)
        dealer_score = self._calculate_score(self.dealer_hand)
        player_score = self._calculate_score(self.player_hand)

        table = PrettyTable()
        table.field_names = ["Player", "Score", "Cards"]
        table.add_row(["Dealer", dealer_score, dealer_cards])
        table.add_row(["Player", f"-->{player_score}<--", player_cards])

        status_str = self._game_state.value.replace("_", " ").title()
        return f"||{status_str}||\n\n{table}"

    def player_is_bust(self) -> bool:
        """Returns True if the player is bust, else False."""
        return self._hand_is_bust(self.player_hand)

    def player_hit(self) -> None:
        self._hit_hand(self.player_hand)

        if self.player_is_bust():
            self._game_state = GameState.DEALER_WON

    def _hand_is_bust(self, hand: list[Card]) -> bool:
        """Returns True if the score is over 21, else False."""
        return self._calculate_score(hand) > 21

    def _hit_hand(self, hand: list[Card]) -> None:
        """Adds a card to the given hand."""

        if self._game_state != GameState.IN_PROGRESS:
            raise InvalidMove("Game has already finished")

        if not self._has_dealt_cards:
            raise InvalidMove("Game has not started, initial cards needs to be dealt")

        hand.append(self._deck.draw_card())

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

    def _play_dealer_turn(self) -> None:
        """Executes the dealer's turn after the player stands."""

        if self._game_state != GameState.IN_PROGRESS:
            raise InvalidMove("Game has already finished")

        dealer_score = self._calculate_score(self.dealer_hand)

        # Dealer's turn
        while dealer_score < 17:
            self._hit_hand(self.dealer_hand)
            dealer_score = self._calculate_score(self.dealer_hand)

        player_score = self._calculate_score(self.player_hand)

        if player_score > 21:
            self._game_state = GameState.DEALER_WON
        elif dealer_score > 21:
            self._game_state = GameState.PLAYER_WON
        elif dealer_score > player_score:
            self._game_state = GameState.DEALER_WON
        elif dealer_score < player_score:
            self._game_state = GameState.PLAYER_WON
        else:
            self._game_state = GameState.DRAW
