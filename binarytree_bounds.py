from typing import List, Optional, Tuple

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
    """
    Perform DFS to find the minimum and maximum values in the subtree rooted at node.
    """
    if not node:
        # float('inf') should be used to represent the smallest possible value when looking for the minimum.
        # float('-inf') should be used to represent the largest possible value when looking for the maximum.
        # This means that if the node is None (i.e., when a subtree does not exist), it should contribute an 
        # "infinite minimum" and a "negative infinite maximum" to ensure correct comparisons in the tree traversal.
        return float('inf'), float('-inf')
    # Recursion on left and right subtrees
    left_min, left_max = dfs(node.left)
    right_min, right_max = dfs(node.right)
    # Find min and max values for the current subtree
    min_val = min(node.val, left_min, right_min)
    max_val = max(node.val, left_max, right_max)
    return min_val, max_val

def find_min_max(root: Optional[TreeNode]) -> List[int]:
    """
    Find the smallest and largest values in the binary tree.
    """
    if not root:
        return [-1, -1]
    # DFS to find minimum and maximum values
    smallest, largest = dfs(root)
    # Adjust for the case where `-1` is used to represent missing nodes
    if smallest == float('inf'):
        smallest = -1
    if largest == float('-inf'):
        largest = -1
    return [smallest, largest]

# Function to build a complete binary tree from a list of values
def build_complete_binary_tree(values: List[int]) -> Optional[TreeNode]:
    """
    Construct a complete binary tree from a list of values.
    `-1` represents a missing node.
    """
    if not values:
        return None
    nodes = [None if val == -1 else TreeNode(val) for val in values]
    root = nodes[0]
    for i in range(len(values)):
        if nodes[i] is not None:
            left_index = 2 * i + 1
            right_index = 2 * i + 2
            if left_index < len(values):
                nodes[i].left = nodes[left_index]
            if right_index < len(values):
                nodes[i].right = nodes[right_index]
    return root

# Example usage:
# Constructing a complete binary tree from a list:
# [5, 3, 8, 1, 4, -1, 9]
# This represents the following tree:
#        5
#       / \
#      3   8
#     / \   \
#    1   4   9

values = [5, 3, 8, 1, 4, -1, 9]
root = build_complete_binary_tree(values)
result = find_min_max(root)
print(f"Smallest and largest nodes in the binary tree: {result}")
