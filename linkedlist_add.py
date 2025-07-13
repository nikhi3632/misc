from typing import Optional
import unittest

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbersBackwardStore(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            # Get values or 0 if list ended
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Compute sum and carry
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # Add to result list
            current.next = ListNode(digit)
            current = current.next

            # Advance input lists
            if l1: l1 = l1.next
            if l2: l2 = l2.next
        return dummy.next
    
    def addTwoNumbersForwardStore(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        stack1 = []
        stack2 = []

        # Push all nodes to stacks
        while l1:
            stack1.append(l1.val)
            l1 = l1.next
        while l2:
            stack2.append(l2.val)
            l2 = l2.next

        carry = 0
        head = None  # head of result list

        while stack1 or stack2 or carry:
            val1 = stack1.pop() if stack1 else 0
            val2 = stack2.pop() if stack2 else 0
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # Create new node and link it in front
            new_node = ListNode(digit)
            new_node.next = head
            head = new_node
        return head

def list_to_linkedlist(items):
    dummy = ListNode()
    current = dummy
    for x in items:
        current.next = ListNode(x)
        current = current.next
    return dummy.next

def linkedlist_to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result
  
class TestAddTwoNumbers(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_backward_store_case1(self):
        l1 = list_to_linkedlist([2, 4, 3])  # 342
        l2 = list_to_linkedlist([5, 6, 4])  # 465
        result = self.solution.addTwoNumbersBackwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [7, 0, 8])  # 807

    def test_backward_store_with_carry(self):
        l1 = list_to_linkedlist([9, 9, 9])  # 999
        l2 = list_to_linkedlist([1])        # 1
        result = self.solution.addTwoNumbersBackwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [0, 0, 0, 1])  # 1000

    def test_forward_store_case1(self):
        l1 = list_to_linkedlist([7, 2, 4, 3])  # 7243
        l2 = list_to_linkedlist([5, 6, 4])     # 564
        result = self.solution.addTwoNumbersForwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [7, 8, 0, 7])  # 7807

    def test_forward_store_with_carry(self):
        l1 = list_to_linkedlist([9, 9])  # 99
        l2 = list_to_linkedlist([1])     # 1
        result = self.solution.addTwoNumbersForwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [1, 0, 0])  # 100

    def test_forward_store_same_length(self):
        l1 = list_to_linkedlist([1, 2, 3])
        l2 = list_to_linkedlist([4, 5, 6])
        result = self.solution.addTwoNumbersForwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [5, 7, 9])  # 123 + 456 = 579

    def test_backward_store_same_length(self):
        l1 = list_to_linkedlist([1, 2, 3])
        l2 = list_to_linkedlist([7, 5, 6])
        result = self.solution.addTwoNumbersBackwardStore(l1, l2)
        self.assertEqual(linkedlist_to_list(result), [8, 7, 9])  # 321 + 657 = 978

    def test_backward_store_empty_lists(self):
        result = self.solution.addTwoNumbersBackwardStore(None, None)
        self.assertEqual(linkedlist_to_list(result), [])

    def test_forward_store_empty_lists(self):
        result = self.solution.addTwoNumbersForwardStore(None, None)
        self.assertEqual(linkedlist_to_list(result), [])

if __name__ == '__main__':
    unittest.main()
