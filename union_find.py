import random

class UnionFind: # Disjoint Set Union or Union Find by Rank
    def __init__(self, n):
        self.parentNode = list(range(n))  # Each node starts as its own parent
        self.treeRank = [1] * n           # Each tree starts with rank 1

    def find(self, node):
        # Path Compression: Point each node directly to its root
        if self.parentNode[node] != node:
            self.parentNode[node] = self.find(self.parentNode[node])
        return self.parentNode[node]

    def union(self, nodeA, nodeB):
        rootA = self.find(nodeA)
        rootB = self.find(nodeB)

        if rootA != rootB:  # Only merge if they are in different sets
            # Union by Rank: Attach the smaller tree under the larger one
            if self.treeRank[rootA] > self.treeRank[rootB]:
                self.parentNode[rootB] = rootA
            elif self.treeRank[rootA] < self.treeRank[rootB]:
                self.parentNode[rootA] = rootB
            else:
                if random.choice([True, False]):  # Choose randomly between True (rootA) or False (rootB)
                    self.parentNode[rootB] = rootA
                    self.treeRank[rootA] += 1  # Increase the rank of rootA when attaching rootB to rootA
                else:
                    self.parentNode[rootA] = rootB
                    self.treeRank[rootB] += 1  # Increase the rank of rootB when attaching rootA to rootB

    def getSetsInfo(self):
        # This function returns a dictionary with root nodes as keys
        # and corresponding height (rank) and members (list of nodes) of each set as values.
        set_info = {}
        for i in range(len(self.parentNode)):
            root = self.find(i)
            # Initialize the set entry if not already present
            if root not in set_info:
                set_info[root] = {'height': self.treeRank[root], 'members': []}
            # Add the current node to the list of members for the set
            set_info[root]['members'].append(i)
        return set_info

if __name__ == "__main__":
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    sets_info = uf.getSetsInfo()
    print(sets_info)
