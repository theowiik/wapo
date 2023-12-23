import unittest
from src.blackjack.blackjack import Card, Deck, Blackjack, Suite

class TestCard(unittest.TestCase):
    def test_create_card_with_suit_and_rank(self):
        card = Card(Suite.CLUBS, "A")
        self.assertEqual(card.suit, Suite.CLUBS)
        self.assertEqual(card.rank, "A")

class TestDeck(unittest.TestCase):
    def test_initialize_deck_with_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck._cards), 52)

    def test_draw_card_reduces_deck_size_by_one(self):
        deck = Deck()
        drawn_card = deck.draw_card()
        self.assertIsInstance(drawn_card, Card)
        self.assertEqual(len(deck._cards), 51)

class TestBlackjack(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack()

    def test_deal_initial_two_cards_each_to_player_and_dealer(self):
        self.game._deal_cards()
        self.assertEqual(len(self.game.player_hand), 2)
        self.assertEqual(len(self.game.dealer_hand), 2)

    def test_hit_adds_one_card_to_player_hand(self):
        self.game._deal_cards()
        self.game.hit(self.game.player_hand)
        self.assertEqual(len(self.game.player_hand), 3)

    def test_calculate_score_of_hand(self):
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        score = self.game._calculate_score(self.game.player_hand)
        self.assertEqual(score, 21)

    def test_check_if_hand_score_exceeds_21(self):
        self.game.player_hand = [Card(Suite.HEARTS, "10"), Card(Suite.SPADES, "J"), Card(Suite.CLUBS, "5")]
        score = self.game._calculate_score(self.game.player_hand)
        self.assertTrue(self.game._is_bust(score))

if __name__ == "__main__":
    unittest.main()
