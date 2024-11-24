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
            self.system_empty_determinator = buffer[0][1][0]
            root_children = self._prepare_nodes(self.system_empty_determinator, buffer)
            for child in root_children:
                root.append_child(child)

        self.root = root


    def _prepare_nodes(self, target: str | None, data: [(int, [str])]) -> [DisplayFileNode]:
        indices_to_remove = []
        results = []

        for i, entry in enumerate(data):
            # File
            if len(entry[1]) == 1:
                results.append(DisplayFileNode(int(entry[0]), entry[1][-1]))
                entry[1].remove(entry[1][0])
                indices_to_remove.append(i)

            # Folder
            elif entry[1][0] == target and target != self.system_empty_determinator:
                # Take file or folder if it's new
                if not any(entry[1][1] == result.file_name for result in results):
                    # If there are only filename and folder - it's final file and it has heat
                    results.append(DisplayFileNode(int(entry[0]) if len(entry[1]) == 2 else 0, entry[1][1]))
                entry[1].remove(entry[1][0])

            # First pass
            elif entry[1][0] == self.system_empty_determinator:

                # Take file or folder if it's new
                if not any(entry[1][1] == result.file_name for result in results):
                    # For files - remove and add hit count, for folders count = 0 and do not remove
                    is_file = len(entry[1]) == 2
                    results.append(DisplayFileNode(int(entry[0]) if is_file else 0, entry[1][1]))
                    entry[1].remove(entry[1][1]) if is_file else None

                # Remove determinator
                entry[1].remove(entry[1][0])
                if len(entry[1]) == 0:
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
