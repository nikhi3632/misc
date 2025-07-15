'''
LRU Cache Design & Implementation

✅ 1. Goals of the Design
    The implementation aims to satisfy the following:
        O(1) get() and put() operations
        Least Recently Used (LRU) eviction policy
        TTL (Time To Live) support for expiring keys
        Thread safety for concurrent access
        Resizable capacity without breaking the cache

✅ 2. Core Data Structures
    ➤ Doubly Linked List
        Maintains the order of usage from Most Recently Used (MRU) to Least Recently Used (LRU).
        Nodes are moved to the head on every access (get) or update (put).
        Eviction always happens at the tail.

    ➤ Hash Map (Dictionary)
        Maps keys to their corresponding linked list nodes for O(1) access.
        Each node also contains its expiry timestamp (TTL).

    ➤ threading.Lock
        Ensures thread-safe mutation and access of shared structures (cache, list pointers).

✅ 3. Design Decisions
    ➤ Dummy Head & Tail Nodes
        Used in the linked list to avoid edge-case handling when adding/removing head/tail.
        head <-> node1 <-> node2 <-> ... <-> nodeN <-> tail
        This ensures all operations like insert/remove happen uniformly.

    ➤ TTL Stored in Node
        Each node has an expire_at timestamp.
        This avoids maintaining a separate TTL map and simplifies eviction checks.

✅ 4. Operation Details
    get(key)
        Check if key exists in the hash map.
        If not → return -1 (miss).
        If expired → remove node, delete from map, return -1.
        If valid → move to front of list (mark MRU), return value.

    put(key, value, ttl)
        Calculate expire_at = now + ttl.
        If key exists:
        Update value and TTL.
        Move node to front (MRU).
        If key doesn't exist:
        Create a new node, add to list head, update map.
        Call _evict_expired() to remove old/expired entries.
        If capacity exceeded, evict tail node (LRU).

    _evict_expired()
        Walk backward from tail and remove any expired nodes.
        Stops as soon as a non-expired node is found (since newer nodes are closer to head).

    resize(new_capacity)
        Adjusts self.capacity.
        Removes expired and extra LRU nodes if needed.

✅ 5. Thread Safety
    All public methods (get, put, resize) are wrapped in a with self.lock: block using threading.Lock.
    This ensures:
        No two threads mutate the structure concurrently.
        No race conditions in the cache dictionary or linked list pointers.
        Lock granularity is coarse (full method), which is safe and simple.

✅ 6. Time Complexity
    Operation	                Time Complexity
    get(key)	                O(1)
    put(key, value, ttl)	    O(1)
    resize(new_capacity)	    O(k) where k = # of evictions (usually small)
    _evict_expired()	        O(k) — lazy removal during operations
    
    Most operations stay at amortized O(1), unless many expired nodes accumulate.
'''

import time
import threading

class Node:
    def __init__(self, key, value, expire_at):
        self.key = key
        self.value = value
        self.expire_at = expire_at
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node(0, 0, 0)
        self.tail = Node(0, 0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = threading.Lock()  # Lock for thread safety

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _is_expired(self, node: Node):
        return node.expire_at < time.time()

    def _evict_expired(self):
        current: Node = self.tail.prev
        while current != self.head:
            if self._is_expired(current):
                prev = current.prev
                self._remove(current)
                del self.cache[current.key]
                current = prev
            else:
                break

    def get(self, key: int) -> int:
        with self.lock:
            if key not in self.cache:
                return -1
            node: Node = self.cache[key]
            if self._is_expired(node):
                self._remove(node)
                del self.cache[key]
                return -1
            self._remove(node)
            self._add_to_head(node)
            return node.value

    def put(self, key: int, value: int, ttl: int):
        now = time.time()
        expire_at = now + ttl

        with self.lock:
            if key in self.cache:
                node: Node = self.cache[key]
                node.value = value
                node.expire_at = expire_at
                self._remove(node)
                self._add_to_head(node)
            else:
                node = Node(key, value, expire_at)
                self.cache[key] = node
                self._add_to_head(node)

            self._evict_expired()

            while len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

    def resize(self, new_capacity: int):
        with self.lock:
            self.capacity = new_capacity
            self._evict_expired()
            while len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

import unittest

class TestLRUCache(unittest.TestCase):

    def setUp(self):
        self.lru_cache = LRUCache(3)

    # Smoke Test
    def test_initialization(self):
        self.assertIsNotNone(self.lru_cache)

    # Sanity Test
    def test_basic_put_get(self):
        self.lru_cache.put(1, 100, ttl=5)
        self.assertEqual(self.lru_cache.get(1), 100)

    # Unit Test - TTL expiration
    def test_ttl_expiry(self):
        self.lru_cache.put(1, 100, ttl=1)
        time.sleep(1.5)
        self.assertEqual(self.lru_cache.get(1), -1)

    # Unit Test - Overwriting keys
    def test_update_value_resets_ttl(self):
        self.lru_cache.put(1, 100, ttl=5)
        self.lru_cache.put(1, 200, ttl=5)
        self.assertEqual(self.lru_cache.get(1), 200)

    # Functional Test - Resize capacity
    def test_resize_eviction(self):
        self.lru_cache.put(1, 1, ttl=5)
        self.lru_cache.put(2, 2, ttl=5)
        self.lru_cache.put(3, 3, ttl=5)
        self.lru_cache.resize(2)
        self.assertEqual(len(self.lru_cache.cache), 2)

    # Functional Test - LRU eviction
    def test_lru_eviction(self):
        self.lru_cache.put(1, 1, ttl=5)
        self.lru_cache.put(2, 2, ttl=5)
        self.lru_cache.put(3, 3, ttl=5)
        self.lru_cache.get(1)  # use key 1
        self.lru_cache.put(4, 4, ttl=5)  # should evict key 2
        self.assertEqual(self.lru_cache.get(2), -1)
        self.assertEqual(self.lru_cache.get(1), 1)

    # Regression Test - Resize after expiry
    def test_resize_after_expired(self):
        self.lru_cache.put(1, 1, ttl=1)
        self.lru_cache.put(2, 2, ttl=1)
        time.sleep(1.5)
        self.lru_cache.resize(1)
        self.assertEqual(len(self.lru_cache.cache), 0)

    # Cache Hit/Miss
    def test_cache_hit_miss(self):
        self.lru_cache.put(1, 100, ttl=5)
        self.assertEqual(self.lru_cache.get(1), 100)  # Hit
        self.assertEqual(self.lru_cache.get(2), -1)   # Miss

    # Concurrency Test
    def test_concurrent_access(self):
        def writer():
            for i in range(100):
                self.lru_cache.put(i, i*10, ttl=2)

        def reader():
            for i in range(100):
                self.lru_cache.get(i)

        threads = []
        for _ in range(5):
            t1 = threading.Thread(target=writer)
            t2 = threading.Thread(target=reader)
            threads.extend([t1, t2])

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Check that no errors occurred and cache size is within bounds
        self.assertLessEqual(len(self.lru_cache.cache), self.lru_cache.capacity)

    # End-to-End Test
    def test_end_to_end_flow(self):
        self.lru_cache.put(1, 100, ttl=2)
        self.lru_cache.put(2, 200, ttl=2)
        self.lru_cache.put(3, 300, ttl=2)
        self.assertEqual(self.lru_cache.get(1), 100)
        self.lru_cache.put(4, 400, ttl=2)  # Should evict key 2
        self.assertEqual(self.lru_cache.get(2), -1)
        time.sleep(2.1)
        self.assertEqual(self.lru_cache.get(1), -1)
        self.lru_cache.resize(1)
        self.assertLessEqual(len(self.lru_cache.cache), 1)

    # Stress Test
    def test_stress_under_load(self):
        for i in range(1000):
            self.lru_cache.put(i, i * 10, ttl=1)
            self.lru_cache.get(i)
        time.sleep(1.1)
        # After TTL, all entries should expire
        expired = sum(1 for i in range(1000) if self.lru_cache.get(i) == -1)
        self.assertGreater(expired, 900)

    # Performance Test (basic timing)
    def test_performance(self):
        start = time.time()
        for i in range(500):
            self.lru_cache.put(i, i, ttl=10)
            self.lru_cache.get(i)
        duration = time.time() - start
        self.assertLess(duration, 2, "Cache is too slow for 500 ops")

if __name__ == '__main__':
    unittest.main()
