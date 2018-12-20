from collections import OrderedDict


class IndexedOrderedDict(OrderedDict):
    """
    An Indexed OrderedDict

    can use dict[0], dict[1] to get items
    """

    def __getitem__(self, key):
        if isinstance(key, int):
            i = 0
            for v in self.values():
                if i == key:
                    return v
                i = i + 1
        return super().__getitem__(key)
