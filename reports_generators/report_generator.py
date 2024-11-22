from abc import ABC, abstractmethod


class ReportGenerator(ABC):

    @abstractmethod
    def generate(self) -> None:
        pass