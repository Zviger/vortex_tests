import json
from pathlib import Path
from re import findall
from typing import List
from dataclasses import asdict

import json2html

from .entities import TestSet, Test
from .logger import get_logger

STATUS_MAP = {
    1: "FAILED",
    0: "PASSED"
}


class Visualizer:
    logger = get_logger()

    @classmethod
    def create_report(cls, js, report_folder: str) -> str:
        report_folder = Path(report_folder)
        if not report_folder.exists():
            raise cls.logger.error(f"This directory not exists: {report_folder}")
        if not report_folder.is_dir():
            raise cls.logger.error(f"Is not a directory: {report_folder}")

        file_id = cls.get_next_file_index(report_folder)

        report_file_path = str(report_folder.joinpath(f"{file_id}.html"))
        with open(report_file_path, "w") as f:
            f.write(json2html.json2html.convert(json=js))
        return report_file_path

    @classmethod
    def create_test_sets_report(cls, test_sets: List[TestSet], report_folder: str) -> str:

        test_set_dicts = list(map(asdict, test_sets))
        for test_set_dict in test_set_dicts:
            for test in test_set_dict["tests"]:
                test["status"] = STATUS_MAP[test["status"]]
        js = json.dumps(test_set_dicts, default=str)

        return cls.create_report(js, report_folder)

    @staticmethod
    def get_next_file_index(folder: Path) -> int:

        file_indexes = []
        for file in folder.iterdir():
            file_index = findall(r"(\d+).html", file.name)
            if file_index:
                file_indexes.append(int(file_index[0]))
        file_indexes = sorted(file_indexes)
        current_index = 0
        for index in file_indexes:
            if index - current_index > 1:
                break
            else:
                current_index = index
        return current_index + 1

    @classmethod
    def create_tests_report(cls, tests: List[Test], report_folder: str, ) -> str:

        test_dicts = list(map(asdict, tests))
        for test in test_dicts:
            test["status"] = STATUS_MAP[test["status"]]
        js = json.dumps(test_dicts, default=str)

        return cls.create_report(js, report_folder)
