from copy import deepcopy


class PrototypeMixin:

    def clone(self):
        return deepcopy(self)
