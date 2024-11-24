import {IRenderable} from "./irenderable";
import {BREAD_CRUMB_TARGET} from "../consts";

export class BreadCrumb implements IRenderable {
    private path: string;
    private container: HTMLElement;
    private readonly className: string;

    constructor() {
        this.path = "";
        this.className = "path-breadCrumb";
    }

    public afterInitiated(container: HTMLElement): void {
        this.container = container;

        let targets = this.container.getElementsByClassName(BREAD_CRUMB_TARGET);

        for (let i = 0; i < targets.length; i++) {
            let target = targets[i];

            target.addEventListener('mouseenter', (e) => {
                const path: string = target.getAttribute('data-path');
                this.setPath(path);
            });
        }

    }

    public setPath(path: string): void {
        this.path = path;
        this.container.getElementsByClassName(this.className)[0]
            .innerHTML = this.getPathRendered();
    }

    public render(): string {
        const renderedPath = this.getPathRendered();
        return `
            <div class=${this.className}>
                ${renderedPath}
            </div>
        `;
    }

    private getPathRendered(): string {
        const segments = (this.path || '').split('/');
        return `
                ${segments.map((segment, index) => `
                    <span class="path-segment" data-path="${segments.slice(0, index + 1).join('/')}">${segment}</span>
                    ${index < segments.length - 1 ? '<span class="path-separator">/</span>' : ''}
                `).join('')}
        `
    }
}