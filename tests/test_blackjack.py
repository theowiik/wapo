import unittest
from src.blackjack.blackjack_core import Card, Deck, Blackjack, InvalidMove, Suite


class TestCard(unittest.TestCase):
    def test_error_on_invalid_suit_creation(self):
        with self.assertRaises(ValueError):
            Card("InvalidSuit", "A")

        with self.assertRaises(ValueError):
            Card(None, "A")

        with self.assertRaises(ValueError):
            Card("", "A")

    def test_error_on_invalid_rank_creation(self):
        with self.assertRaises(ValueError):
            Card(Suite.CLUBS, "InvalidRank")

    def test_card_string_representation_format(self):
        card = Card(Suite.HEARTS, "10")
        self.assertEqual(str(card), "10 of Hearts")


class TestDeck(unittest.TestCase):
    def test_error_when_drawing_from_empty_deck(self):
        deck = Deck()
        deck._cards = []  # Empty the deck
        with self.assertRaises(IndexError):
            deck.draw_card()

    def test_deck_order_changes_after_shuffle(self):
        deck = Deck()
        before_shuffle = deck._cards.copy()
        deck.shuffle()
        self.assertNotEqual(before_shuffle, deck._cards)


class TestBlackjack(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack()

    def test_error_when_hitting_after_bust(self):
        self.game._deal_cards()
        self.game.player_hand = [
            Card(Suite.HEARTS, "10"),
            Card(Suite.SPADES, "J"),
            Card(Suite.CLUBS, "5"),
        ]
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)

    def test_bust_scenario_with_aces_in_hand(self):
        self.game.player_hand = [
            Card(Suite.HEARTS, "A"),
            Card(Suite.SPADES, "J"),
            Card(Suite.CLUBS, "A"),
            Card(Suite.DIAMONDS, "8"),
        ]
        score = self.game._calculate_score(self.game.player_hand)
        self.assertTrue(self.game._is_bust(score))

    def test_score_calculation_with_multiple_aces(self):
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "A")]
        score = self.game._calculate_score(self.game.player_hand)
        self.assertEqual(score, 12)

    def test_blackjack_with_two_cards(self):
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        score = self.game._calculate_score(self.game.player_hand)
        self.assertEqual(score, 21)

    def test_dealer_behavior_on_soft_17(self):
        # Assuming the game logic makes the dealer hit on soft 17
        self.game.dealer_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "6")]
        self.game._dealer_play()
        self.assertGreater(len(self.game.dealer_hand), 2)

    def test_ensure_start_game_before_hit(self):
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)

    def test_ensure_start_game_before_stand(self):
        with self.assertRaises(InvalidMove):
            self.game.player_stand()

    def test_cant_hit_after_stand(self):
        self.game.deal_cards()
        self.game.player_stand()
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)

    def test_cant_stand_after_stand(self):
        self.game.deal_cards()
        self.game.player_stand()
        with self.assertRaises(InvalidMove):
            self.game.player_stand()

    def test_cant_deal_cards_after_stand(self):
        self.game.deal_cards()
        self.game.player_stand()
        with self.assertRaises(InvalidMove):
            self.game._deal_cards()

    def test_cant_deal_cards_after_bust(self):
        self.game.deal_cards()
        self.game.player_hand = [
            Card(Suite.HEARTS, "10"),
            Card(Suite.SPADES, "J"),
            Card(Suite.CLUBS, "5"),
        ]
        with self.assertRaises(InvalidMove):
            self.game._deal_cards()

    def test_cant_hit_after_bust(self):
        self.game.deal_cards()
        self.game.player_hand = [
            Card(Suite.HEARTS, "10"),
            Card(Suite.SPADES, "J"),
            Card(Suite.CLUBS, "5"),
        ]
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)

    def test_cant_stand_after_bust(self):
        self.game.deal_cards()
        self.game.player_hand = [
            Card(Suite.HEARTS, "10"),
            Card(Suite.SPADES, "J"),
            Card(Suite.CLUBS, "5"),
        ]
        with self.assertRaises(InvalidMove):
            self.game.player_stand()

    def test_cant_hit_after_blackjack(self):
        self.game.deal_cards()
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)

    def test_cant_stand_after_blackjack(self):
        self.game._deal_cards()
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        with self.assertRaises(InvalidMove):
            self.game.player_stand()

    def test_cant_deal_cards_after_blackjack(self):
        self.game.deal_cards()
        self.game.player_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        with self.assertRaises(InvalidMove):
            self.game._deal_cards()

    def test_cant_hit_after_dealer_stand(self):
        self.game.deal_cards()
        self.game.dealer_hand = [Card(Suite.HEARTS, "A"), Card(Suite.SPADES, "J")]
        self.game._dealer_play()
        with self.assertRaises(InvalidMove):
            self.game._hit_hand(self.game.player_hand)


if __name__ == "__main__":
    unittest.main()
