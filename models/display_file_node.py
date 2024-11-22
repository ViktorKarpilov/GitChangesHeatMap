from dataclasses import dataclass, field
from functools import reduce
from typing import Callable


@dataclass
class DisplayFileNode:
    _occurrence_count: int
    file_name: str
    expanded: bool = False
    _parent: 'DisplayFileNode' = None
    _children: list['DisplayFileNode'] = field(default_factory=list)

    def unwrap(self) -> list['DisplayFileNode']:
        self.expanded = True
        result = [self]
        result.extend(target.unwrap() for target in self._children)
        return result

    def append_child(self, child: 'DisplayFileNode') -> None:
        child._parent = self
        self._children.append(child)

    def get_children(self) -> list['DisplayFileNode']:
        return self._children

    def get_heat(self) -> int:
        reducer: Callable[[int, 'DisplayFileNode'], int] = lambda value, node: value + node.get_heat()
        return reduce(reducer, self._children, self._occurrence_count)

    def is_child(self, target: 'DisplayFileNode') -> bool:
        return self._parent == target
