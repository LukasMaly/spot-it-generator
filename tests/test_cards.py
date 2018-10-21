import unittest

from cards import is_prime, create_cards


class TestCards(unittest.TestCase):
    """Tests functions in module cards"""
    def test_is_prime(self):
        primes = [0, 1, 2, 3, 5, 7, 11]
        non_primes = [4, 6, 8, 10]
        for i in primes:
            self.assertTrue(is_prime(i))
        for i in non_primes:
            self.assertFalse(is_prime(i))

    def test_create_cards_primes(self):
        primes = [0, 1, 2, 3, 5, 7, 11]
        for i in primes:
            _, _ = create_cards(i)

    def test_create_cards_non_primes(self):
        non_primes = [4, 6, 8, 10]
        for i in non_primes:
            with self.assertRaises(ValueError):
                _, _ = create_cards(i)

    def test_create_cards_num_pictures(self):
        orders = [0, 1, 2, 3, 5, 7, 11]
        nums = [1, 3, 7, 13, 31, 57, 133]
        for order, num in zip(orders, nums):
            _, num_pictures = create_cards(order)
            self.assertEqual(num, num_pictures)


if __name__ == '__main__':
    unittest.main()
