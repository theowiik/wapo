from blackjack.blackjack_core import Blackjack, GameState


class BlackjackInterface:
    """
    One instance per game.
    1 player vs dealer.
    """

    def __init__(self) -> None:
        self.game: Blackjack = Blackjack()

    def deal_cards(self) -> None:
        self.game.deal_cards()

    def hit(self) -> None:
        self.game._hit_hand(self.game.player_hand)

    def stand(self) -> None:
        self.game.player_stand()

    def display(self) -> str:
        return self.game.display()

    def check_player_bust(self) -> bool:
        return self.game.player_is_bust()

    def get_state(self) -> GameState:
        return self.game._game_state
