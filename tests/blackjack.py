import unittest

from src.blackjack.blackjack import Card, Deck, Blackjack


class TestBlackjack(unittest.TestCase):
    def test_card_creation(self):
        card = Card("Hearts", "A")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.rank, "A")

    def test_deck_creation(self):
        deck = Deck()
        self.assertEqual(len(deck._cards), 52)
        self.assertIn(Card("Hearts", "A"), deck._cards)

    def test_deal_cards(self):
        game = Blackjack()
        game._deal_cards()
        self.assertEqual(len(game.player_hand), 2)
        self.assertEqual(len(game.dealer_hand), 2)

    def test_hit_method(self):
        game = Blackjack()
        game.hit(game.player_hand)
        self.assertEqual(len(game.player_hand), 1)

    def test_stand_method(self):
        game = Blackjack()
        game._deal_cards()
        result, player_score, dealer_score = game.stand()
        self.assertTrue(
            result in ["Player wins", "Dealer wins", "It's a tie", "Dealer busts"]
        )

    def test_score_calculation(self):
        game = Blackjack()
        game.player_hand = [Card("Hearts", "A"), Card("Diamonds", "K")]
        score = game._calculate_score(game.player_hand)
        self.assertEqual(score, 21)

        game.player_hand = [Card("Hearts", "A"), Card("Diamonds", "9")]
        score = game._calculate_score(game.player_hand)
        self.assertEqual(score, 20)

    def test_game_outcomes(self):
        game = Blackjack()
        game.player_hand = [Card("Hearts", "10"), Card("Diamonds", "K")]
        game.dealer_hand = [Card("Clubs", "9"), Card("Spades", "6")]
        result, _, _ = game.stand()
        self.assertEqual(result, "Player wins")

        game.player_hand = [
            Card("Hearts", "5"),
            Card("Diamonds", "K"),
            Card("Spades", "8"),
        ]
        game.dealer_hand = [Card("Clubs", "9"), Card("Spades", "6")]
        result, _, _ = game.stand()
        self.assertEqual(result, "Dealer wins")

        game.player_hand = [Card("Hearts", "10"), Card("Diamonds", "K")]
        game.dealer_hand = [Card("Clubs", "10"), Card("Spades", "K")]
        result, _, _ = game.stand()
        self.assertEqual(result, "It's a tie")


if __name__ == "__main__":
    unittest.main()
