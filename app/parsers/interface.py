from abc import ABC, abstractmethod

from app.entities import TestSet


class Parser(ABC):

    @staticmethod
    @abstractmethod
    def parse_stdout(stdout: str) -> TestSet:
        pass
