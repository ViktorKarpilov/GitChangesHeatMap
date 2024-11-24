import {IRenderable} from "./irenderable";
import {FileExplorerState, FileNode} from "../states";
import {BREAD_CRUMB_TARGET} from "../consts";

export class FileExplorer implements IRenderable{
    private data: FileNode;
    private state: FileExplorerState;
    private nodeClassName: string;

    constructor(data: FileNode) {
        this.data = data;
        this.state = {
            searchTerm: "",
            sortBy: "name",
            selectedNode: null,
            sortDirection: "desc",
        }
        this.nodeClassName = "node"
    }

    afterInitiated(container: HTMLElement): void {
        let root = (document.querySelector(`.${this.nodeClassName}`) as HTMLElement);
        this.coupleRenderedAndDataNodes(root, this.data)

        this.traverseNodes(this.data, (node) => {
            node.renderedNode.addEventListener("click", (e) => {
                e.stopPropagation();
                if(node.children.length){
                    node.expanded = !node.expanded;
                    node.renderedNode.classList.toggle("collapsed");
                }
            })
        })

        container.querySelector(".file-explorer > button")
            .addEventListener("click", (e) => { this.toggleAll(); });
    }

    public render(): string {
        return `
            <div class="file-explorer">
                <button data-action="expand">Toggle All</button>
                ${this.renderTree(this.data)}
            </div>
        `;
    }

    private coupleRenderedAndDataNodes(rendered_node: HTMLElement, data_node: FileNode): void {
        data_node.renderedNode = rendered_node;
        let data_children = data_node.children;

        let rendered_parent_childrens = rendered_node.children;
        let rendered_childrens: HTMLCollectionOf<HTMLElement>;
        for (let i = 0; i < rendered_parent_childrens.length; i++) {
            if(rendered_parent_childrens[i].className == "children"){
                rendered_childrens = rendered_parent_childrens[i].children as HTMLCollectionOf<HTMLElement>;
                break;
            }
        }

        if(rendered_childrens){
            for (let i = 0; i < rendered_childrens.length; i++) {
                let id = parseInt(rendered_childrens[i].id);
                // Rendered children would always have same children as data. If we start from root - there always will be
                // at least 1 children we want
                let children = data_children.filter(data => data.id == id)[0];
                this.coupleRenderedAndDataNodes(rendered_childrens[i], children)
            }

            return;
        }
    }

    private renderTree(node: FileNode): string {
        const isSelected = this.state.selectedNode === node;

        return `
            <div id="${node.id}" class="${this.nodeClassName} ${node.expanded ? 'expanded' : 'collapsed'} ${isSelected ? 'selected' : ''} ${BREAD_CRUMB_TARGET}"
                 data-path="${node.path}">
                <div class="node-content" style="background-color: ${node.color}">
                    ${node.children.length ? '<span class="arrow">▼</span>' : '<span class="arrow"></span>'}
                    <span class="icon">${node.children.length ? '📁' : '📄'}</span>
                    <span class="name">${node.fileName}</span>
                    <span class="count">${node.occurrenceCount}</span>
                </div>
                ${node.children.length ? `
                    <div class="children">
                        ${node.children
            .map(child => this.renderTree(child))
            .join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }

    // If root open - close all, if closed - open all
    public toggleAll(): void {
        this.traverseNodes(this.data, (node) => {
            node.expanded = !this.data.expanded;
            if(node.expanded){
                node.renderedNode.classList.remove("collapsed");
            }
            else{
                node.renderedNode.classList.add("collapsed")
            }
        });
    }

    public filterNodes(searchTerm: string, targetNode: FileNode = null): boolean {
        const termLower = searchTerm.toLowerCase();

        if (!targetNode){
            return this.filterNodes(termLower, this.data);
        }

        // Do not search for less than 4 and if cleaned - refresh
        if (!searchTerm || searchTerm.length < 4){
            if(searchTerm.length < 2){
                this.traverseNodes(this.data, node => node.renderedNode.classList.remove("hidden"));
            }
        }

        let isMatch = false;

        // Need to iterate all in order to collapse non matching
        for (let i = 0; i < targetNode.children.length; i++) {
            isMatch = this.filterNodes(termLower, targetNode.children[i]) || isMatch;
        }
        isMatch = isMatch || this.isIncludeString(targetNode.path, termLower);

        if(!isMatch){
            targetNode.renderedNode.classList.add("hidden");
        }

        return isMatch;
    }

    public sortNodes(sortBy: 'name' | 'count', direction: 'asc' | 'desc'): void {
        this.traverseNodes(this.data, (node) => {
            if (node.children.length === 0) return;

            const childrenContainer = node.renderedNode.querySelector('.children');
            if (!childrenContainer) return;

            // Sort the children array
            node.children.sort((a, b) => {
                let comparison: number;
                if (sortBy === 'name') {
                    comparison = a.fileName.localeCompare(b.fileName);
                } else {
                    comparison = a.occurrenceCount - b.occurrenceCount;
                }
                return direction === 'asc' ? comparison : -comparison;
            });

            // Rearrange DOM elements without recreating them
            const fragment = document.createDocumentFragment();
            node.children.forEach(child => {
                fragment.appendChild(child.renderedNode);
            });
            childrenContainer.innerHTML = ''; // Clear container
            childrenContainer.appendChild(fragment);
        });
    }

    private traverseNodes(node: FileNode, callback: (node: FileNode) => void): void {
        callback(node);
        node.children.forEach((child:FileNode) => this.traverseNodes(child, callback));
    }

    private isIncludeString(first:string, second:string): boolean {
        return first.indexOf(second) !== -1;
    }
}