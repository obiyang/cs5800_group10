import unittest
from word_prediction import Trie, edit_distance, spell_correction

class TestTrie(unittest.TestCase):
    def setUp(self):
        # Create a new Trie instance and insert some sample words with frequencies.
        self.trie = Trie()
        self.trie.insert("apple", 10)        # Highest frequency
        self.trie.insert("app", 5)
        self.trie.insert("application", 8)   # Second highest frequency

    def test_autocomplete_existing_prefix(self):
        # Test for a prefix that exists in the Trie.
        # Expected order is based on descending frequency: "apple" (10), "application" (8), then "app" (5)
        expected = ["apple", "application", "app"]
        result = self.trie.autocomplete("app")
        self.assertEqual(result, expected, "Autocomplete failed to sort results by frequency.")

    def test_autocomplete_non_existing_prefix(self):
        # Test for a prefix that does not exist in the Trie.
        result = self.trie.autocomplete("xyz")
        self.assertEqual(result, [], "Autocomplete should return an empty list for non-existent prefixes.")

class TestEditDistance(unittest.TestCase):
    def test_edit_distance_values(self):
        # Verify that known edit distances match expected values.
        self.assertEqual(edit_distance("kitten", "sitting"), 3, "Edit distance between 'kitten' and 'sitting' should be 3.")
        self.assertEqual(edit_distance("apple", "apple"), 0, "Edit distance for identical words should be 0.")
        self.assertEqual(edit_distance("flaw", "lawn"), 2, "Edit distance between 'flaw' and 'lawn' should be 2.")

class TestSpellCorrection(unittest.TestCase):
    def test_spell_correction_suggestions(self):
        # Define a small dictionary for testing.
        dictionary = ["apple", "apply", "ample", "maple"]
        # Input word with a minor error.
        word = "appl"
        suggestions = spell_correction(word, dictionary)
        # Check that one of the closest matches is returned. Here, we expect "apple" or "apply" as suggestions.
        self.assertTrue(any(sugg in suggestions for sugg in ["apple", "apply"]),
                        "Spell correction did not return the expected close match.")

if __name__ == '__main__':
    unittest.main()
