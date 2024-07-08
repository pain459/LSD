import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f'{node}:{i}')
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        keys_to_redistribute = []
        for i in range(self.replicas):
            key = self._hash(f'{node}:{i}')
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)
        self.sorted_keys.sort()
        return keys_to_redistribute

    def get_nodes(self, key, num_replicas=2):
        if not self.ring:
            return []
        hash_key = self._hash(key)
        nodes = []
        for i in range(num_replicas):
            idx = bisect.bisect(self.sorted_keys, hash_key) % len(self.sorted_keys)
            nodes.append(self.ring[self.sorted_keys[idx]])
            hash_key += 1
        return nodes
