from .blackjack_models import GameState
from .blackjack_impl import BlackjackImpl


class Blackjack:
    """
    One instance per game. 1 player only.

    Rules:
        - Player is dealt 2 cards
        - Dealer is dealt 1 card
        - Player can hit or stand, no other options
        - Once player stands, dealer plays
        - Dealer stands on 17

        - Win conditions:
            - Player gets 21
            - Player gets higher than dealer
            - Dealer goes bust
            - Tie if both player and dealer have same score, including 21
    """

    def __init__(self) -> None:
        self.game: BlackjackImpl = BlackjackImpl()

    def deal_cards(self) -> None:
        self.game.deal_cards()

    def hit(self) -> None:
        self.game.player_hit()

    def stand(self) -> None:
        self.game.player_stand()

    def display(self) -> str:
        return self.game.display()

    def is_bust(self) -> bool:
        return self.game.player_is_bust()

    def get_state(self) -> GameState:
        return self.game._game_state
