import csv
from pathlib import Path

from reports_generators.web_report_generator import WebReportGenerator
from models.display_file_node import DisplayFileNode
from models.display_window import DisplayWindow


class Solution:
    def __init__(self):
        # TODO input of that
        self.csv_path = "heatmap-data.csv"

    def _get_nodes(self):
        with open(self.csv_path) as f:
            reader = csv.DictReader(f)
            root = DisplayFileNode(0, ".")

            # Could be big but i`m to stupid to create algorythm to add node by node them
            buffer = [(row["Count"], list(Path(row['File']).parts)) for row in reader]
            root_children = self._prepare_nodes(None, buffer)
            for child in root_children:
                root.append_child(child)

        self.root = root


    def _prepare_nodes(self, target: str | None, data: [(int, [str])]) -> [DisplayFileNode]:
        indices_to_remove = []
        results = []

        for i, entry in enumerate(data):
            if (target is None and len(entry[1]) == 1) or (target is not None and entry[0] == target):
                results.append(DisplayFileNode(int(entry[0]), entry[1][-1]))
                indices_to_remove.append(i)

        # Remove from end to not mess up indices
        for i in reversed(indices_to_remove):
            data.pop(i)

        results_number = len(results)
        for i in range(results_number):
            result = results[i]
            result_children = self._prepare_nodes(result.file_name, data)
            for child in result_children:
                result.append_child(child)

        return results

    def initiate_web_solution(self):
        self._get_nodes()
        window = DisplayWindow([self.root])
        WebReportGenerator(window).generate()
