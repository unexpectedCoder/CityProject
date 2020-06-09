from space import Space

from copy import copy


class Scene:
    def __init__(self, space: Space):
        self.space = copy(space)
