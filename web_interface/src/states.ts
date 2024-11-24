export interface FileNode {
    fileName: string;
    occurrenceCount: number;
    expanded: boolean;
    children: FileNode[];
    path?: string;
    color?: string;
    id?: number;
    renderedNode?: HTMLElement;
}

export interface FileExplorerState {
    searchTerm: string;
    selectedNode: FileNode | null;
    sortBy: 'name' | 'count' | 'size';
    sortDirection: 'asc' | 'desc';
}

export interface ToolbarState {
    searchTerm: string;
    sortBy: 'name' | 'count' | 'size';
    sortDirection: 'asc' | 'desc';
}
