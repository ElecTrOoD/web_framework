from copy import deepcopy, copy


class PrototypeMixin:

    def clone(self):
        return copy(self)
