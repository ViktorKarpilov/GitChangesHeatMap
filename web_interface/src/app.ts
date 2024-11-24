import {FileExplorerBuilder} from "./models/file_explorer_builder";
import {BreadCrumb} from "./models/bread_crumb";
import {Toolbar} from "./models/toolbar";
import {Renderer} from "./utils/renderer";

document.addEventListener('DOMContentLoaded', () => {
    const explorer = new FileExplorerBuilder().build();
    const breadCrumb = new BreadCrumb();
    const toolBar = new Toolbar(explorer);

    const renderer = new Renderer(breadCrumb, toolBar, explorer);
});
