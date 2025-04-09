# CS5800 Final Project
# Word Prediction and Spell Correction Algorithms

from typing import List, Tuple

# ----------------------------
# Trie Tree for Autocomplete
# ----------------------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # For sorting later

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, freq: int = 0):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency = freq

    def _dfs(self, node: TrieNode, prefix: str, results: List[Tuple[str, int]]):
        if node.is_end_of_word:
            results.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

    def autocomplete(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._dfs(node, prefix, results)
        # Sort using frequency descending (Greedy component)
        results.sort(key=lambda x: -x[1])
        return [word for word, freq in results]


# ------------------------------------
# Edit Distance for Spell Correction
# ------------------------------------
def edit_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Delete
                    dp[i][j - 1],    # Insert
                    dp[i - 1][j - 1] # Replace
                )
    return dp[m][n]


def spell_correction(word: str, dictionary: List[str]) -> List[str]:
    distances = [(w, edit_distance(word, w)) for w in dictionary]
    distances.sort(key=lambda x: x[1])
    min_dist = distances[0][1] if distances else float('inf')
    return [w for w, d in distances if d == min_dist]


# ----------------------------
# Example Usage
# ----------------------------
if __name__ == "__main__":
    words_with_freq = [
        ("hello", 20),
        ("help", 15),
        ("hell", 5),
        ("helmet", 10),
        ("helicopter", 8),
        ("hero", 12),
    ]
    
    trie = Trie()
    for word, freq in words_with_freq:
        trie.insert(word, freq)

    print("Autocomplete suggestions for 'hel':")
    print(trie.autocomplete("hel"))

    test_word = "helo"
    print(f"\nSpelling correction for '{test_word}':")
    print(spell_correction(test_word, [w for w, _ in words_with_freq]))
