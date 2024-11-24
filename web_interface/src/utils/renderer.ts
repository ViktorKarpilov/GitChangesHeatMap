import {BreadCrumb} from "../models/bread_crumb";
import {FileExplorer} from "../models/file_explorer";
import {Toolbar} from "../models/toolbar";
import {CONTAINER_ID} from "../consts";
import {IRenderable} from "../models/irenderable";

// I don't care is it expandable
export class Renderer {
    private readonly orderedElements: IRenderable[];
    private container: HTMLElement;

    constructor(breadCrumb: BreadCrumb, toolbar: Toolbar, fileExplorer: FileExplorer) {
        this.orderedElements = [
            toolbar,
            breadCrumb,
            fileExplorer
        ]
        this.container = document.getElementById(CONTAINER_ID)
        this.renderApp()
        this.orderedElements.forEach(orderedElement => orderedElement.afterInitiated(this.container))
    }

    private renderApp() : void{
        let html = ''
        for (const element of this.orderedElements) {
            html += `\n${element.render()}\n`
        }
        this.container.innerHTML = html;
    }

    public attachEventListeners(): void {
        const searchBox = this.container.querySelector('.search-box') as HTMLInputElement;
        // searchBox?.addEventListener('input', (e) => {
        //     this.state.searchTerm = (e.target as HTMLInputElement).value;
        //     this.renderApp();
        // });
        //
        // this.container.querySelectorAll('.sort-button').forEach(button => {
        //     button.addEventListener('click', () => {
        //         const sortType = button.getAttribute('data-sort') as 'name' | 'count';
        //         if (this.state.sortBy === sortType) {
        //             this.state.sortDirection = this.state.sortDirection === 'asc' ? 'desc' : 'asc';
        //         } else {
        //             this.state.sortBy = sortType;
        //             this.state.sortDirection = 'asc';
        //         }
        //         this.render();
        //     });
        // });
        //
        // document.querySelectorAll('button').forEach(button => {
        //     button.addEventListener('click', (e) => {
        //         const action = button.getAttribute('data-action');
        //         if (action === 'expand') {
        //             explorer.expandAll();
        //         } else if (action === 'collapse') {
        //             explorer.collapseAll();
        //         }
        //     });
        // });
    }
}
