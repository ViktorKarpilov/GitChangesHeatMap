import webbrowser
from argparse import ArgumentError
from pathlib import Path

from reports_generators.report_generator import ReportGenerator
from models.display_file_node_web_view_template import DisplayFileNodeWebViewTemplate
from models.display_window import DisplayWindow
from web_interface.web_components import WebComponents


class WebReportGenerator(ReportGenerator):
    def __init__(self, display_window: DisplayWindow):
        self.display_window = display_window

    def generate(self) -> None:
        root = list(filter(lambda x: x.is_child(None),self.display_window.get_nodes()))

        if len(root) != 1:
            raise ArgumentError("Fatal error - invalid data structure. Multiple root nodes found.")

        root = root[0]

        js_data_template = """
            console.log("Data script start");
            const data = %s;
            localStorage.setItem("HEATMAP_DATA",JSON.stringify(data));
            console.log("Data saved to localStorage");
        """
        js_data = DisplayFileNodeWebViewTemplate(root).render()
        js_data = js_data_template % (js_data,)

        html_data = WebComponents().get_html()
        html_data = html_data.replace("{{js_data_code}}", js_data)

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_data)

        file_path = Path('index.html').absolute().as_uri()
        if webbrowser.open(file_path):
            print("Report generated successfully")
        else:
            print("Could not open browser")