import {FileNode} from "../states";

export interface TreeOperations {
    filterTree(node: FileNode, searchTerm: string): FileNode | null;
    sortTree(node: FileNode, sortBy: 'name' | 'count', direction: 'asc' | 'desc'): FileNode;
}

export class FileTreeOperations implements TreeOperations {
    // Deep clone a node and its children
    private cloneNode(node: FileNode): FileNode {
        return {
            ...node,
            children: node.children.map(child => this.cloneNode(child)),
            // Don't clone the rendered node as it will be recreated
            renderedNode: undefined
        };
    }

    // Filter tree based on search term
    public filterTree(node: FileNode, searchTerm: string): FileNode | null {
        if (!searchTerm) return this.cloneNode(node);

        const termLower = searchTerm.toLowerCase();
        const nodeMatch = node.fileName.toLowerCase().match(termLower) ||
            node.path.toLowerCase().match(termLower);

        // Clone the current node
        const filteredNode = this.cloneNode(node);

        // Filter children
        filteredNode.children = node.children
            .map(child => this.filterTree(child, searchTerm))
            .filter((child): child is FileNode => child !== null);

        // Keep this node if it matches or has matching children
        if (nodeMatch || filteredNode.children.length > 0) {
            // If there's a match, expand the node to show the matching content
            filteredNode.expanded = true;
            return filteredNode;
        }

        return null;
    }

    // Sort tree based on criteria
    public sortTree(node: FileNode, sortBy: 'name' | 'count', direction: 'asc' | 'desc'): FileNode {
        const sortedNode = this.cloneNode(node);

        // Sort children recursively
        sortedNode.children = sortedNode.children
            .map(child => this.sortTree(child, sortBy, direction))
            .sort((a, b) => {
                let comparison: number;

                if (sortBy === 'name') {
                    comparison = a.fileName.localeCompare(b.fileName);
                } else { // sortBy === 'count'
                    comparison = a.occurrenceCount - b.occurrenceCount;
                }

                return direction === 'asc' ? comparison : -comparison;
            });

        return sortedNode;
    }
}