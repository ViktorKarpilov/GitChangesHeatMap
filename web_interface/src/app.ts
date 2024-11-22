interface TreeNode {
    fileName: string;
    occurrenceCount: number;
    expanded: false,
    children: TreeNode[];
}

class TreeExplorer {
    private maxCount: number;
    private root: HTMLElement;

    constructor(containerId: string, data: TreeNode) {
        this.root = document.getElementById(containerId) as HTMLElement;
        if (!this.root) throw new Error(`Container ${containerId} not found`);
        this.maxCount = this.findMaxCount(data);
        this.render(data);
    }

    private findMaxCount(node: TreeNode): number {
        let max = node.occurrenceCount || 0;
        if (node.children) {
            node.children.forEach(child => {
                max = Math.max(max, this.findMaxCount(child));
            });
        }
        return max;
    }

    private getColorForCount(count: number): string {
        const normalized = count / this.maxCount;
        const red = Math.floor(normalized * 255);
        const green = Math.floor((1 - normalized) * 255);
        return `rgb(${red}, ${green}, 0)`;
    }

    private createNode(node: TreeNode): HTMLElement {
        const div = document.createElement('div');
        div.className = 'node';
        
        const content = document.createElement('div');
        content.className = 'node-content';
        
        const toggle = document.createElement('span');
        toggle.className = 'toggle';
        
        const name = document.createElement('span');
        name.textContent = node.fileName;
        
        const count = document.createElement('span');
        count.className = 'count';
        count.textContent = node.occurrenceCount?.toString() || '0';
        
        content.append(toggle, name, count);
        div.appendChild(content);
        
        if (node.children?.length) {
            toggle.textContent = '+';
            
            const children = document.createElement('div');
            children.className = 'children';
            
            node.children.forEach(child => {
                children.appendChild(this.createNode(child));
            });
            
            div.appendChild(children);
            
            toggle.addEventListener('click', (e: Event) => {
                e.stopPropagation();
                children.classList.toggle('open');
                toggle.textContent = children.classList.contains('open') ? '-' : '+';
            });
        }
        
        if (node.occurrenceCount) {
            div.style.backgroundColor = this.getColorForCount(node.occurrenceCount);
        }
        
        return div;
    }

    private render(data: TreeNode): void {
        this.root.appendChild(this.createNode(data));
    }
}
console.log("Loaded")

document.addEventListener('DOMContentLoaded', () => {
    const data = JSON.parse(localStorage.getItem("HEATMAP_DATA")) as TreeNode;
    new TreeExplorer('explorer', data);
});