from dataclasses import dataclass, field

from models.display_file_node import DisplayFileNode


@dataclass
class DisplayWindow:
    # Ordered list for display a.k state
    _nodes: list[DisplayFileNode] = field(default_factory=list)

    def toggle_node(self, target_node: DisplayFileNode) -> None:
        node_index:int = self._nodes.index(target_node)
        node = self._nodes[node_index]
        node.expanded = not node.expanded

        if node.expanded:
            self._nodes[node_index:node_index] = node.get_children()
            return

        for x in self._nodes[::-1]:
            if x.is_child(node):
                self._nodes.remove(x)

    def get_nodes(self) -> list[DisplayFileNode]:
        return self._nodes
