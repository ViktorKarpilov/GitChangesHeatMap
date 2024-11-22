from models.display_file_node import DisplayFileNode

DEFAULT_DISPLAY_NODE_TEMPLATE = """
{
    fileName: "%s",
    occurrenceCount: %s,
    expanded: %s,
    children: [
        %s
    ]
}
"""

class DisplayFileNodeWebViewTemplate:
    def __init__(self, node: DisplayFileNode):
        self.node = node

    def render(self) -> str:
        children_string = ""

        for children in self.node.get_children():
            if len(children_string) > 0:
                children_string += ", "

            children_string += DisplayFileNodeWebViewTemplate(children).render()

        node = DEFAULT_DISPLAY_NODE_TEMPLATE % (
           self.node.file_name,          # %s for fileName
           self.node.get_heat(),   # %s for occurrenceCount
           str(self.node.expanded).lower(),  # %s for expanded (converts Python True/False to JS true/false)
           children_string     # %s for children content
        )

        return node