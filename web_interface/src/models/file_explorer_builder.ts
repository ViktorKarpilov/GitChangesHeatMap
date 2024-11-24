import {FileExplorer} from "./file_explorer";
import {FileNode} from "../states";

export class FileExplorerBuilder {
    private readonly data: FileNode;
    private readonly maxCount: number;
    private referenceNumber: { number: number; };

    constructor() {
        this.referenceNumber = { number: 0 };
        this.data = this.loadData();
        this.maxCount = this.calculateMaxCount(this.data);
        this.calculateDynamic(this.data);
    }

    private loadData(): FileNode {
        const rawData = localStorage.getItem("HEATMAP_DATA");
        let data : FileNode = rawData ? JSON.parse(rawData) : {
            fileName: ".",
            occurrenceCount: 1,
            expanded: true,
            children: []
        };
        return data
    }

    // private getBackgroundColor(count: number): string {
    //     if (this.maxCount === 0) return 'transparent';
    //     const ratio = count / this.maxCount;
    //     const red = Math.floor(255 * ratio);
    //     const green = Math.floor(255 * (1 - ratio));
    //     return `rgba(${red}, ${green}, 0, 0.1)`;
    // }

    private getBackgroundColor(count: number): string {
        if (this.maxCount === 0) return 'transparent';

        const logMax = Math.log(this.maxCount + 1);
        const logCount = Math.log(count + 1);
        const ratio = logCount / logMax;

        const red = Math.floor(255 * ratio);
        const green = Math.floor(255 * (1 - Math.pow(ratio, 2)));

        return `rgba(${red}, ${green}, 0, 0.3)`;
    }


    private calculateDynamic(node: FileNode, parentPath: string = ""): void {
        const currentPath = parentPath ? `${parentPath}/${node.fileName}` : node.fileName;
        node.path = currentPath;
        node.color = this.getBackgroundColor(node.occurrenceCount);

        node.id = this.referenceNumber.number;
        this.referenceNumber.number += 1;

        node.children.forEach(child => this.calculateDynamic(child, currentPath));
    }

    private calculateMaxCount(node: FileNode): number {
        let max = node.occurrenceCount;
        for (const child of node.children) {
            max = Math.max(max, this.calculateMaxCount(child));
        }
        return max;
    }

    public build(): FileExplorer {
        return new FileExplorer(this.data);
    }
}