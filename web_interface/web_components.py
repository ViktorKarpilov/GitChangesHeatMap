# Auto edited content
class WebComponents:
    def __init__(self):
        self.__html_content = r"""<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Changes Heat Map</title>

        <!-- placeholder for test - remove after push -->
        <script src="temp.js"></script>
        <script src="test_data.js"></script>
        <link rel="stylesheet" href="style.css">
        <style>

            :root {
    --transition-duration: 0.3s;
    --border-radius: 6px;
    --spacing-unit: 8px;
    --primary-color: #2196f3;
    --hover-color: rgba(33, 150, 243, 0.1);
}

body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 20px;
}

.file-explorer {
    background: white;
    border-radius: var(--border-radius);
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.toolbar {
    display: flex;
    gap: var(--spacing-unit);
    margin-bottom: 20px;
    padding: var(--spacing-unit);
    background: #f8f9fa;
    border-radius: var(--border-radius);
}

.search-box {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: var(--border-radius);
    font-size: 14px;
}

button {
    padding: 8px 12px;
    background: white;
    border: 1px solid #ddd;
    border-radius: var(--border-radius);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
}

.sort-button:hover {
    background: var(--hover-color);
}

.node {
    margin: 2px 0;
    border-radius: var(--border-radius);
}

.node-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-unit);
    padding: 8px;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all var(--transition-duration);
}

.node-content:hover {
    background: var(--hover-color);
}

.node.selected > .node-content {
    background: var(--hover-color);
    border: 1px solid var(--primary-color);
}

.children {
    margin-left: 24px;
    border-left: 2px solid #eee;
    padding-left: var(--spacing-unit);
    overflow: hidden;
    transition: max-height var(--transition-duration) ease-in-out;
}

.collapsed > .children {
    max-height: 0;
}

.expanded > .children {
    max-height: 1000px;
}

.arrow {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform var(--transition-duration);
}

.collapsed > .node-content > .arrow {
    transform: rotate(-90deg);
}

.icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
}

.count {
    margin-left: auto;
    font-size: 0.9em;
    color: #666;
    background: #f8f9fa;
    padding: 2px 8px;
    border-radius: 12px;
}

.details-panel {
    background: white;
    border-radius: var(--border-radius);
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.details-panel h2 {
    margin-top: 0;
    font-size: 1.2em;
    color: #333;
}

.details-item {
    margin: 12px 0;
}

.details-label {
    font-weight: 500;
    color: #666;
    margin-bottom: 4px;
}

.details-value {
    color: #333;
}

.path-breadcrumb {
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 8px;
    background: #f8f9fa;
    border-radius: var(--border-radius);
    margin-bottom: 12px;
    overflow-x: auto;
}

.path-segment {
    color: #666;
    cursor: pointer;
}

.path-segment:hover {
    color: var(--primary-color);
}

.path-separator {
    color: #999;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

.node-enter {
    animation: fadeIn var(--transition-duration) ease-out;
}

.hidden {
    display: none !important;
}

        </style>

        <!-- placeholder for production compiled js do not touch -->
        <script>
            {{js_data_code}}

            (() => {
  // web_interface/src/consts.ts
  var CONTAINER_ID = "app_container";
  var BREAD_CRUMB_TARGET = "breadCrumb-target";

  // web_interface/src/models/file_explorer.ts
  var FileExplorer = class {
    data;
    state;
    nodeClassName;
    constructor(data) {
      this.data = data;
      this.state = {
        searchTerm: "",
        sortBy: "name",
        selectedNode: null,
        sortDirection: "desc"
      };
      this.nodeClassName = "node";
    }
    afterInitiated(container) {
      let root = document.querySelector(`.${this.nodeClassName}`);
      this.coupleRenderedAndDataNodes(root, this.data);
      this.traverseNodes(this.data, (node) => {
        node.renderedNode.addEventListener("click", (e) => {
          e.stopPropagation();
          if (node.children.length) {
            node.expanded = !node.expanded;
            node.renderedNode.classList.toggle("collapsed");
          }
        });
      });
      container.querySelector(".file-explorer > button").addEventListener("click", (e) => {
        this.toggleAll();
      });
    }
    render() {
      return `
            <div class="file-explorer">
                <button data-action="expand">Toggle All</button>
                ${this.renderTree(this.data)}
            </div>
        `;
    }
    coupleRenderedAndDataNodes(rendered_node, data_node) {
      data_node.renderedNode = rendered_node;
      let data_children = data_node.children;
      let rendered_parent_childrens = rendered_node.children;
      let rendered_childrens;
      for (let i = 0; i < rendered_parent_childrens.length; i++) {
        if (rendered_parent_childrens[i].className == "children") {
          rendered_childrens = rendered_parent_childrens[i].children;
          break;
        }
      }
      if (rendered_childrens) {
        for (let i = 0; i < rendered_childrens.length; i++) {
          let id = parseInt(rendered_childrens[i].id);
          let children = data_children.filter((data) => data.id == id)[0];
          this.coupleRenderedAndDataNodes(rendered_childrens[i], children);
        }
        return;
      }
    }
    renderTree(node) {
      const isSelected = this.state.selectedNode === node;
      return `
            <div id="${node.id}" class="${this.nodeClassName} ${node.expanded ? "expanded" : "collapsed"} ${isSelected ? "selected" : ""} ${BREAD_CRUMB_TARGET}"
                 data-path="${node.path}">
                <div class="node-content" style="background-color: ${node.color}">
                    ${node.children.length ? '<span class="arrow">\u25BC</span>' : '<span class="arrow"></span>'}
                    <span class="icon">${node.children.length ? "\u{1F4C1}" : "\u{1F4C4}"}</span>
                    <span class="name">${node.fileName}</span>
                    <span class="count">${node.occurrenceCount}</span>
                </div>
                ${node.children.length ? `
                    <div class="children">
                        ${node.children.map((child) => this.renderTree(child)).join("")}
                    </div>
                ` : ""}
            </div>
        `;
    }
    // If root open - close all, if closed - open all
    toggleAll() {
      this.traverseNodes(this.data, (node) => {
        node.expanded = !this.data.expanded;
        if (node.expanded) {
          node.renderedNode.classList.remove("collapsed");
        } else {
          node.renderedNode.classList.add("collapsed");
        }
      });
    }
    filterNodes(searchTerm, targetNode = null) {
      const termLower = searchTerm.toLowerCase();
      if (!targetNode) {
        return this.filterNodes(termLower, this.data);
      }
      if (!searchTerm || searchTerm.length < 4) {
        if (searchTerm.length < 2) {
          this.traverseNodes(this.data, (node) => node.renderedNode.classList.remove("hidden"));
        }
      }
      let isMatch = false;
      for (let i = 0; i < targetNode.children.length; i++) {
        isMatch = this.filterNodes(termLower, targetNode.children[i]) || isMatch;
      }
      isMatch = isMatch || this.isIncludeString(targetNode.path, termLower);
      if (!isMatch) {
        targetNode.renderedNode.classList.add("hidden");
      }
      return isMatch;
    }
    sortNodes(sortBy, direction) {
      this.traverseNodes(this.data, (node) => {
        if (node.children.length === 0) return;
        const childrenContainer = node.renderedNode.querySelector(".children");
        if (!childrenContainer) return;
        node.children.sort((a, b) => {
          let comparison;
          if (sortBy === "name") {
            comparison = a.fileName.localeCompare(b.fileName);
          } else {
            comparison = a.occurrenceCount - b.occurrenceCount;
          }
          return direction === "asc" ? comparison : -comparison;
        });
        const fragment = document.createDocumentFragment();
        node.children.forEach((child) => {
          fragment.appendChild(child.renderedNode);
        });
        childrenContainer.innerHTML = "";
        childrenContainer.appendChild(fragment);
      });
    }
    traverseNodes(node, callback) {
      callback(node);
      node.children.forEach((child) => this.traverseNodes(child, callback));
    }
    isIncludeString(first, second) {
      return first.indexOf(second) !== -1;
    }
  };

  // web_interface/src/models/file_explorer_builder.ts
  var FileExplorerBuilder = class {
    data;
    maxCount;
    referenceNumber;
    constructor() {
      this.referenceNumber = { number: 0 };
      this.data = this.loadData();
      this.maxCount = this.calculateMaxCount(this.data);
      this.calculateDynamic(this.data);
    }
    loadData() {
      const rawData = localStorage.getItem("HEATMAP_DATA");
      let data = rawData ? JSON.parse(rawData) : {
        fileName: ".",
        occurrenceCount: 1,
        expanded: true,
        children: []
      };
      return data;
    }
    // private getBackgroundColor(count: number): string {
    //     if (this.maxCount === 0) return 'transparent';
    //     const ratio = count / this.maxCount;
    //     const red = Math.floor(255 * ratio);
    //     const green = Math.floor(255 * (1 - ratio));
    //     return `rgba(${red}, ${green}, 0, 0.1)`;
    // }
    getBackgroundColor(count) {
      if (this.maxCount === 0) return "transparent";
      const logMax = Math.log(this.maxCount + 1);
      const logCount = Math.log(count + 1);
      const ratio = logCount / logMax;
      const red = Math.floor(255 * ratio);
      const green = Math.floor(255 * (1 - Math.pow(ratio, 2)));
      return `rgba(${red}, ${green}, 0, 0.3)`;
    }
    calculateDynamic(node, parentPath = "") {
      const currentPath = parentPath ? `${parentPath}/${node.fileName}` : node.fileName;
      node.path = currentPath;
      node.color = this.getBackgroundColor(node.occurrenceCount);
      node.id = this.referenceNumber.number;
      this.referenceNumber.number += 1;
      node.children.forEach((child) => this.calculateDynamic(child, currentPath));
    }
    calculateMaxCount(node) {
      let max = node.occurrenceCount;
      for (const child of node.children) {
        max = Math.max(max, this.calculateMaxCount(child));
      }
      return max;
    }
    build() {
      return new FileExplorer(this.data);
    }
  };

  // web_interface/src/models/bread_crumb.ts
  var BreadCrumb = class {
    path;
    container;
    className;
    constructor() {
      this.path = "";
      this.className = "path-breadCrumb";
    }
    afterInitiated(container) {
      this.container = container;
      let targets = this.container.getElementsByClassName(BREAD_CRUMB_TARGET);
      for (let i = 0; i < targets.length; i++) {
        let target = targets[i];
        target.addEventListener("mouseenter", (e) => {
          const path = target.getAttribute("data-path");
          this.setPath(path);
        });
      }
    }
    setPath(path) {
      this.path = path;
      this.container.getElementsByClassName(this.className)[0].innerHTML = this.getPathRendered();
    }
    render() {
      const renderedPath = this.getPathRendered();
      return `
            <div class=${this.className}>
                ${renderedPath}
            </div>
        `;
    }
    getPathRendered() {
      const segments = (this.path || "").split("/");
      return `
                ${segments.map((segment, index) => `
                    <span class="path-segment" data-path="${segments.slice(0, index + 1).join("/")}">${segment}</span>
                    ${index < segments.length - 1 ? '<span class="path-separator">/</span>' : ""}
                `).join("")}
        `;
    }
  };

  // web_interface/src/models/toolbar.ts
  var debounceTimeout;
  var Toolbar = class {
    state;
    fileExplorer;
    constructor(fileExplorer) {
      this.fileExplorer = fileExplorer;
      this.state = {
        searchTerm: "",
        sortBy: "name",
        sortDirection: "desc"
      };
    }
    afterInitiated(self) {
      const searchBox = self.querySelector(".search-box");
      searchBox?.addEventListener("input", (e) => {
        this.state.searchTerm = e.target.value;
        this.debounce((term) => {
          this.fileExplorer.filterNodes(term);
        }, 300)(this.state.searchTerm);
      });
      self.querySelectorAll(".sort-button").forEach((button) => {
        button.addEventListener("click", () => {
          const sortType = button.getAttribute("data-sort");
          if (this.state.sortBy === sortType) {
            this.state.sortDirection = this.state.sortDirection === "asc" ? "desc" : "asc";
          } else {
            this.state.sortBy = sortType;
            this.state.sortDirection = "asc";
          }
          self.querySelectorAll(".sort-button").forEach((btn) => {
            const btnType = btn.getAttribute("data-sort");
            const iconSpan = btn.querySelector(".sort-icon");
            if (iconSpan) {
              iconSpan.textContent = this.getSortIcon(btnType);
            }
          });
          this.fileExplorer.sortNodes(this.state.sortBy, this.state.sortDirection);
        });
      });
    }
    render() {
      return `
            <div class="toolbar">
                <input type="text" 
                    class="search-box" 
                    placeholder="Search files..." 
                    value="${this.state.searchTerm}">
                <button class="sort-button" data-sort="name">
                    Name <span class="sort-icon">${this.getSortIcon("name")}</span>
                </button>
                <button class="sort-button" data-sort="count">
                    Count <span class="sort-icon">${this.getSortIcon("count")}</span>
                </button>
            </div>
        `;
    }
    debounce(func, wait) {
      return function(...args) {
        if (debounceTimeout) {
          clearTimeout(debounceTimeout);
        }
        debounceTimeout = setTimeout(() => {
          func.apply(this, args);
        }, wait);
      };
    }
    getSortIcon(type) {
      if (this.state.sortBy !== type) return "\u21D5";
      return this.state.sortDirection === "asc" ? "\u21D1" : "\u21D3";
    }
  };

  // web_interface/src/utils/renderer.ts
  var Renderer = class {
    orderedElements;
    container;
    constructor(breadCrumb, toolbar, fileExplorer) {
      this.orderedElements = [
        toolbar,
        breadCrumb,
        fileExplorer
      ];
      this.container = document.getElementById(CONTAINER_ID);
      this.renderApp();
      this.orderedElements.forEach((orderedElement) => orderedElement.afterInitiated(this.container));
    }
    renderApp() {
      let html = "";
      for (const element of this.orderedElements) {
        html += `
${element.render()}
`;
      }
      this.container.innerHTML = html;
    }
    attachEventListeners() {
      const searchBox = this.container.querySelector(".search-box");
    }
  };

  // web_interface/src/app.ts
  document.addEventListener("DOMContentLoaded", () => {
    const explorer = new FileExplorerBuilder().build();
    const breadCrumb = new BreadCrumb();
    const toolBar = new Toolbar(explorer);
    const renderer = new Renderer(breadCrumb, toolBar, explorer);
  });
})();

        </script>

    </head>

    <body>
        <div id="app">
            <header class="header">
                <h1>File Explorer</h1>
            </header>
            <!--     reserved        -->
            <div id="app_container"></div>
        </div>
    </body>
</html>"""

    def get_html(self):
        return self.__html_content
