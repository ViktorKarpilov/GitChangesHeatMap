import {IRenderable} from "./irenderable";
import {ToolbarState} from "../states";
import {FileExplorer} from "./file_explorer";

let debounceTimeout: number|undefined;
export class Toolbar implements IRenderable {
    private state: ToolbarState;
    private fileExplorer: FileExplorer;

    constructor(fileExplorer: FileExplorer) {
        this.fileExplorer = fileExplorer;
        this.state = {
            searchTerm: "",
            sortBy: "name",
            sortDirection: "desc",
        }
    }

    public afterInitiated(self: HTMLElement): void {
        const searchBox = self.querySelector('.search-box') as HTMLInputElement;
        searchBox?.addEventListener('input', (e) => {
            this.state.searchTerm = (e.target as HTMLInputElement).value;

            this.debounce((term: string) => {
                this.fileExplorer.filterNodes(term)
            }, 300)(this.state.searchTerm);
        });

        self.querySelectorAll('.sort-button').forEach(button => {
            button.addEventListener('click', () => {
                const sortType = button.getAttribute('data-sort') as 'name' | 'count';
                if (this.state.sortBy === sortType) {
                    this.state.sortDirection = this.state.sortDirection === 'asc' ? 'desc' : 'asc';
                } else {
                    this.state.sortBy = sortType;
                    this.state.sortDirection = 'asc';
                }

                // Update sort icons for all buttons
                self.querySelectorAll('.sort-button').forEach(btn => {
                    const btnType = btn.getAttribute('data-sort');
                    const iconSpan = btn.querySelector('.sort-icon');
                    if (iconSpan) {
                        iconSpan.textContent = this.getSortIcon(btnType as 'name' | 'count');
                    }
                });

                this.fileExplorer.sortNodes(this.state.sortBy, this.state.sortDirection);
            });
        });
    }

    render(): string {
        return `
            <div class="toolbar">
                <input type="text" 
                    class="search-box" 
                    placeholder="Search files..." 
                    value="${this.state.searchTerm}">
                <button class="sort-button" data-sort="name">
                    Name <span class="sort-icon">${this.getSortIcon('name')}</span>
                </button>
                <button class="sort-button" data-sort="count">
                    Count <span class="sort-icon">${this.getSortIcon('count')}</span>
                </button>
            </div>
        `;
    }

    private debounce<T>(func: (...args: T[]) => any, wait: number) {
        return function(...args: T[]) {
            if(debounceTimeout) {
                clearTimeout(debounceTimeout);
            }

            debounceTimeout = setTimeout(() => {
                func.apply(this, args);
            }, wait);
        };
    }


    private getSortIcon(type: 'name' | 'count'): string {
        if (this.state.sortBy !== type) return '⇕';
        return this.state.sortDirection === 'asc' ? '⇑' : '⇓';
    }
}