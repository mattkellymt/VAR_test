class Deep_Dict(object):
    def __init__(self, leaf=None):
        if type(leaf) is not type:
            leaf = lambda: leaf
        self.leaf = leaf
        self.root = {}

    def __len__(self):
        return len(self.root)

    def __bool__(self):
        return bool(self.root)

    def __setitem__(self, keys, value):
        node, last_key = self.find_leaf(keys)
        node[last_key] = value

    def __getitem__(self, keys):
        node, last_key = self.find_leaf(keys)
        if last_key not in node:
            node[last_key] = self.leaf()
        value = node[last_key]
        return value

    def __repr__(self):
        return repr(self.root)

    def __contains__(self, keys):
        if type(keys) is not tuple:
            keys = [keys]
        node = self.root

        for key in keys:
            if key not in node:
                return False
            node = node[key]
        return True

    def pop(self, keys, default=None):
        if not keys in self:
            return default

        node, last_key = self.find_leaf(keys)
        value = node.pop(last_key)
        return value

    def find_leaf(self, keys):
        if type(keys) is not tuple:
            return self.root, keys
        first_keys = keys[:-1]
        last_key = keys[-1]
        node = self.root

        for key in first_keys:
            if key not in node:
                node[key] = Deep_Dict(leaf=self.leaf)
            node = node[key]
        return node, last_key

    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()

    def items(self):
        return self.root.items()

