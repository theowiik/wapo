from blackjack.blackjack_core import Blackjack


class BlackjackInterface:
    def __init__(self):
        self.game: Blackjack = Blackjack()

    def deal_cards(self):
        self.game.deal_cards()

    def player_hit(self):
        self.game._hit_hand(self.game.player_hand)

    def player_stand(self):
        self.game.player_stand()

    def display_game_state(self):
        return self.game.display()

    def check_player_bust(self):
        return self.game.player_is_bust()
