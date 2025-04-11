# CS5800 Final Project
# Word Prediction and Spell Correction Algorithms

from typing import List, Tuple
import pandas as pd

# ---------------------------------------------
# Trie Tree Implementation for Autocomplete
# ---------------------------------------------
class TrieNode:
    def __init__(self):
        # Dictionary to store child nodes (each key is a character)
        self.children = {}
        # Flag indicating the end of a complete word
        self.is_end_of_word = False
        # Frequency value to help prioritize suggestions (e.g., ranking words)
        self.frequency = 0  

class Trie:
    def __init__(self):
        # Initialize the Trie with an empty root node
        self.root = TrieNode()

    def insert(self, word: str, freq: int = 0):
        """
        Inserts a word into the Trie along with its frequency.
        Each character in the word is added as a child node if not already present.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                # Add a new TrieNode if character is not found
                node.children[char] = TrieNode()
            node = node.children[char]
        # Mark the end of a complete word and assign the frequency
        node.is_end_of_word = True
        node.frequency = freq

    def _dfs(self, node: TrieNode, prefix: str, results: List[Tuple[str, int]]):
        """
        Performs a Depth-First Search (DFS) from the given Trie node.
        It accumulates complete words (prefixes where 'is_end_of_word' is True)
        along with their frequency.
        """
        if node.is_end_of_word:
            results.append((prefix, node.frequency))
        # Continue DFS for each child node recursively.
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

    def autocomplete(self, prefix: str) -> List[str]:
        """
        Provides autocomplete suggestions based on the prefix.
        It navigates to the node corresponding to the last character of the prefix,
        then collects all words below that node using DFS, 
        and sorts them based on frequency (higher frequency first).
        """
        node = self.root
        # Traverse the Trie to reach the node corresponding to the prefix
        for char in prefix:
            if char not in node.children:
                return []  # If prefix is not found, return empty list
            node = node.children[char]
        results = []
        # Collect all complete words starting with the given prefix
        self._dfs(node, prefix, results)
        # Sort the results based on frequency in descending order
        results.sort(key=lambda x: -x[1])
        # Return only the words from the sorted results
        return [word for word, freq in results]


# --------------------------------------------------
# Edit Distance Function for Spell Correction
# --------------------------------------------------
def edit_distance(word1: str, word2: str) -> int:
    """
    Compute the edit distance (Levenshtein Distance) between two words.
    This measures the minimum number of single-character insertions, deletions,
    or substitutions required to change word1 into word2.
    """
    m, n = len(word1), len(word2)
    # Create a DP table with (m+1) x (n+1) dimensions
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill in the DP table
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                # If word1 is empty, insert all characters of word2
                dp[i][j] = j
            elif j == 0:
                # If word2 is empty, remove all characters of word1
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                # If last characters are the same, no new cost is incurred
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # If last characters differ, consider insert, delete, and replace operations
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Deletion
                    dp[i][j - 1],    # Insertion
                    dp[i - 1][j - 1] # Replacement
                )
    return dp[m][n]


def spell_correction(word: str, dictionary: List[str]) -> List[str]:
    """
    Finds the closest word(s) to the given input word from the provided dictionary,
    based on the minimum edit distance. It returns all words that share the minimum
    edit distance.
    """
    # Calculate edit distances for each dictionary word compared to the input word.
    distances = [(w, edit_distance(word, w)) for w in dictionary]
    # Sort the results based on edit distance (smallest distance first)
    distances.sort(key=lambda x: x[1])
    # Determine the minimum distance from the sorted distances
    min_dist = distances[0][1] if distances else float('inf')
    # Return all words that have the minimum edit distance
    return [w for w, d in distances if d == min_dist]


# ----------------------------
# Example Usage of the System
# ----------------------------
if __name__ == "__main__":
    # Load the words from the Excel file.
    # The Excel file should contain a 'Word' column and a 'Frequency_Rank' column.
    df = pd.read_excel("500_common_words.xlsx")
    words_with_freq = [(row["Word"], row["Frequency_Rank"]) for index, row in df.iterrows()]
    
    # Create a Trie instance and insert words from the dictionary
    trie = Trie()
    for word, freq in words_with_freq:
        trie.insert(word, freq)

    # Greet the user and prompt for input
    print("Welcome to the Word Prediction and Spell Correction System")
    print("----------------------------------------------------------")
    user_input = input("Enter a word to predict: ")

    # ----------------------------
    # Autocomplete Suggestions
    # ----------------------------
    print("Autocomplete suggestions for '", user_input, "':")
    autocomplete_suggestions = trie.autocomplete(user_input)
    if not autocomplete_suggestions:
        print("No autocomplete suggestions found")
    else:
        print(autocomplete_suggestions)

    # ----------------------------
    # Spell Correction Suggestion
    # ----------------------------
    print(f"\nSpelling correction for '{user_input}':")
    # Build a simple dictionary list from the words loaded
    spelling_correction = spell_correction(user_input, [w for w, _ in words_with_freq])
    if not spelling_correction:
        print("No spelling correction found")
    else:
        print(spelling_correction)

    print("Thank you for using the Word Prediction and Spell Correction System")
