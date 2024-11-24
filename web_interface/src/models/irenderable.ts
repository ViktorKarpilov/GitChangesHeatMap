// Object that knows it's string representation
export interface IRenderable{
    render(): string;
    afterInitiated(self: HTMLElement): void;
}