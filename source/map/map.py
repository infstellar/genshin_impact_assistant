from cached_property import cached_property

from source.map.bigmap.bigmap import BigMap
from source.map.minimap.minimap import MiniMap


class Map:
    @cached_property
    def bigmap(self):
        return BigMap()

    @cached_property
    def minimap(self):
        return MiniMap()
