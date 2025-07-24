import unittest

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.traverse(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None

    def traverse(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.trie.insert("apple")
        self.trie.insert("app")

    def test_insert_and_search_full_word(self):
        self.assertTrue(self.trie.search("apple"))
        self.assertTrue(self.trie.search("app"))

    def test_insert_and_search_prefix(self):
        self.assertTrue(self.trie.startsWith("ap"))
        self.assertFalse(self.trie.search("ap"))

    def test_nonexistent_words(self):
        self.assertFalse(self.trie.search("banana"))
        self.assertFalse(self.trie.startsWith("b"))

    def test_insert_additional_word(self):
        self.trie.insert("bat")
        self.assertTrue(self.trie.search("bat"))
        self.assertTrue(self.trie.startsWith("ba"))

    def test_case_sensitivity(self):
        self.assertFalse(self.trie.search("Apple"))
        self.trie.insert("Apple")
        self.assertTrue(self.trie.search("Apple"))

if __name__ == '__main__':
    unittest.main()
