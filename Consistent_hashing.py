from bisect import bisect, bisect_left, bisect_right
from hashlib import sha256

import requests


class StorageNode:
    files = {}

    def __init__(self, name, host):
        self.name = name
        self.host = host

    def put_file(self, path):
        self.files[path] = path

    def fetch_file(self, path):
        if path in self.files:
            return self.files.get(path)
        else:
            return None


storage_nodes = [
    StorageNode(name='A', host='10.131.213.12'),
    StorageNode(name='B', host='10.131.213.13'),
    StorageNode(name='C', host='10.131.213.14'),
    StorageNode(name='D', host='10.131.213.15'),
    StorageNode(name='E', host='10.131.213.16')]


class ConsistentHash:
    def __init__(self):
        self._total_slots = pow(2, 256)
        self._keys = []
        self._nodes = []

    def add_node(self, node: StorageNode) -> int:
        if len(self._keys) == self._total_slots:
            raise Exception("Hash space is full")

        key = hash_fn256(node.host, self._total_slots)
        index = bisect(self._keys, key)

        if index > 0 and self._keys[index - 1] == key:
            raise Exception("Collision")

        # data migration from old node to new
        self._nodes.insert(index, node)
        self._keys.insert(index, node)

        return key

    def remove_node(self, node: StorageNode) -> int:
        if len(self._keys) == 0:
            raise Exception("Hash space is empty")

        key = hash_fn256(node.host, self._total_slots)
        index = bisect_left(self.keys)

        if index >= len(self._keys) or self._keys[index] != key:
            raise Exception("Node is not found")

        # data migration
        nodeToDelete = self._nodes[index]
        destNode = self._nodes[index + 1]

        self._keys.pop(index)
        self._nodes.pop(index)

        return key

    def assign(self, item: str) -> str:
        key = hash_fn256(str, self._total_slots)
        index = bisect_right(self._keys, key)
        index = index % len(self._keys)

        return self._nodes[index]


def hash_fn256(key, total_slots):
    hsh = sha256()
    bts = bytes(key.encode('utf-8'))
    hsh.update(bts)
    h_digest = hsh.hexdigest()
    return int(h_digest, 16) % total_slots


def upload(path):
    index = hash_fn256(path, total_slots)

    node = storage_nodes[index]
    node.put_file(path)
    return node.name


def fetch(path):
    index = hash_fn256(path)
    node = storage_nodes[index]
    return node.fetch_file(path)


# Main function
if __name__ == '__main__':
    print("Start")
    f1 = "f1.txt"
    f2 = "f2.txt"
    f3 = "f3.txt"
    f4 = "f4.txt"
    f5 = "f5.txt"

    print(upload(f1))
    print(upload(f2))
    print(upload(f3))
    print(upload(f4))
    print(upload(f5))
