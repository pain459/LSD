def synchronize_data(ch, caches, node):
    for key in ch.get_keys(node):
        new_node = ch.get_node(key)
        if new_node != node:
            value = caches[node].get(key)
            caches[new_node].set(key, value)
            caches[node].delete(key)
