import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, replicas=3):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f'{node}:{i}')
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f'{node}:{i}')
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None
        hash_key = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_key) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_all_nodes(self):
        return set(self.ring.values())

    def get_keys(self, node):
        return [k for k, v in self.ring.items() if v == node]
