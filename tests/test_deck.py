from unittest import TestCase
from api import Deck

class TestDeck(TestCase):

    def test_generate(self):
        d = Deck.generate()

        stock = d.get_card_states().count("S")
        self.assertEqual(stock,10,"The value should be 10")

        player1 = d.get_card_states().count("P1H")
        self.assertEqual(player1, 5,"The value should be 5")

        player2 = d.get_card_states().count("P2H")
        self.assertEqual(player2, 5,"The value should be 5")

