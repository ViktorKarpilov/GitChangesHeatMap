# Auto edited content
class WebComponents:
    def __init__(self):
        self.__html_content = """<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Changes Heat Map</title>

        <!-- placeholder for production compiled js do not touch -->
        <script>
            console.log("App script start");
            {{js_data_code}}

            (() => {
  // web_interface/src/app.ts
  var TreeExplorer = class {
    maxCount;
    root;
    constructor(containerId, data) {
      this.root = document.getElementById(containerId);
      if (!this.root) throw new Error(`Container ${containerId} not found`);
      this.maxCount = this.findMaxCount(data);
      this.render(data);
    }
    findMaxCount(node) {
      let max = node.occurrenceCount || 0;
      if (node.children) {
        node.children.forEach((child) => {
          max = Math.max(max, this.findMaxCount(child));
        });
      }
      return max;
    }
    getColorForCount(count) {
      const normalized = count / this.maxCount;
      const red = Math.floor(normalized * 255);
      const green = Math.floor((1 - normalized) * 255);
      return `rgb(${red}, ${green}, 0)`;
    }
    createNode(node) {
      const div = document.createElement("div");
      div.className = "node";
      const content = document.createElement("div");
      content.className = "node-content";
      const toggle = document.createElement("span");
      toggle.className = "toggle";
      const name = document.createElement("span");
      name.textContent = node.fileName;
      const count = document.createElement("span");
      count.className = "count";
      count.textContent = node.occurrenceCount?.toString() || "0";
      content.append(toggle, name, count);
      div.appendChild(content);
      if (node.children?.length) {
        toggle.textContent = "+";
        const children = document.createElement("div");
        children.className = "children";
        node.children.forEach((child) => {
          children.appendChild(this.createNode(child));
        });
        div.appendChild(children);
        toggle.addEventListener("click", (e) => {
          e.stopPropagation();
          children.classList.toggle("open");
          toggle.textContent = children.classList.contains("open") ? "-" : "+";
        });
      }
      if (node.occurrenceCount) {
        div.style.backgroundColor = this.getColorForCount(node.occurrenceCount);
      }
      return div;
    }
    render(data) {
      this.root.appendChild(this.createNode(data));
    }
  };
  console.log("Loaded");
  document.addEventListener("DOMContentLoaded", () => {
    const data = JSON.parse(localStorage.getItem("HEATMAP_DATA"));
    console.log(data);
    new TreeExplorer("explorer", data);
  });
})();

        </script>

    </head>

    <body>
        <div id="explorer"></div>
    </body>
</html>"""

    def get_html(self):
        return self.__html_content