import os
import subprocess
from functools import reduce
from pathlib import Path
from typing import Tuple, List, Optional
import json
from datetime import datetime
import requests

import matplotlib.pyplot as plt

from .migrator import create_tables
from .visualizer import Visualizer
from .entities import TestSet, Test, TestInfo, CoreInfo, TestsSetInfo, TestsSetParams, CommitHash, FilePath, MakeCommand
from .parsers import SimxParser
from .logger import get_logger
from .repository import get_or_create_test_set, find_test_sets, find_tests


class CommandExecuter:
    logger = get_logger()

    @classmethod
    def toolchain_build(cls, docker_folder, docker_context):
        cls.update_submodules()
        docker_file_path = Path(docker_folder).joinpath("toolchain.Dockerfile")
        if not docker_file_path.exists():
            cls.logger.error(f"Dockerfile {docker_file_path} doesn't exist")
            exit(1)
        docker_context_path = Path(docker_context)
        if not docker_context_path.exists():
            cls.logger.error(f"Docker context {docker_context_path} doesn't exist")
            exit(1)
        cls.logger.info(f"Building toolchain. Dockerfile - {docker_file_path}, "
                        f"docker context - {docker_context}")
        os.system(f"docker build -f {docker_file_path} -t vortex_toolchain {docker_context}")

    @classmethod
    def vortex_build(cls, docker_folder, docker_context, docker_compose_file):
        cls.toolchain_build(docker_folder, docker_context)
        docker_compose_file_path = Path(docker_compose_file)
        if not docker_compose_file_path.exists():
            cls.logger.error(f"Docker-compose file {docker_compose_file_path} doesn't exist")
            exit(1)
        cls.logger.info(f"Building vortex. Docker-compose file - {docker_compose_file_path}")
        os.system(f"docker-compose -f {docker_compose_file} build")

    @classmethod
    def update_submodules(cls):
        cls.logger.info("Updating submodules")
        os.system("git submodule update --init --recursive")

    @classmethod
    def migrate(cls):
        cls.logger.info("Migrating database")
        create_tables()

    @staticmethod
    def vortex_start():
        os.system("docker-compose up -d vortex")

    @staticmethod
    def vortex_stop():
        os.system("docker-compose stop")

    @classmethod
    def run_test(cls, test_path, make_command) -> Tuple[str, int]:
        absolute_test_path = Path("/vortexgpgpu/vortex").joinpath(test_path)
        result = subprocess.run(["docker-compose", "exec", "-T",
                                 "vortex", "bash", "-c",
                                 f"cd {absolute_test_path} && make {make_command}"],
                                stdout=subprocess.PIPE)
        return result.stdout.decode(), result.returncode

    @classmethod
    def get_toolchain_commit(cls) -> CommitHash:
        with open("vortex/ci/toolchain_install.sh") as f:
            for line in f.readlines():
                if line.startswith("REPOSITORY"):
                    commit = line.split("/")[-1].strip()
                    request_header = {'Accept': 'application/vnd.github.v3+json'}
                    res = requests.get("https://api.github.com/repos/vortexgpgpu/vortex-toolchain-prebuilt/branches",
                                       headers=request_header)
                    res_json = res.json()
                    for branch in res_json:

                        if commit == branch["name"]:
                            commit = branch["commit"]["sha"]
        return CommitHash(hash=commit)

    @classmethod
    def get_commit_hash_from_folder(cls, folder: str) -> CommitHash:
        result = subprocess.run(["bash", "-c", f"cd {folder} && git rev-parse HEAD"],
                                stdout=subprocess.PIPE)
        return CommitHash(hash=result.stdout.decode().strip())

    @classmethod
    def load_json(cls, path: str):
        try:
            with open(path) as f:
                content = json.load(f)
        except FileNotFoundError as e:
            cls.logger.error(e)
            exit(1)
        return content


    @classmethod
    def get_paths(cls, path: str) -> List[str]:
        return [test_setting["test_path"] for test_setting in cls.load_json(path)]

    @classmethod
    def vortex_run_tests(cls, test_set_path: str):
        tests_settings = cls.load_json(test_set_path)
        cls.logger.info("Testing is started")
        tests_start = datetime.now()
        cls.vortex_start()
        tests = []
        for test_setting in tests_settings:
            test_path = test_setting.get("test_path", "")
            cls.logger.info(f"Processing test with test path - {test_path} is started")
            for make_command in test_setting.get("make_commands", []):
                cls.logger.info(f"Run make command - {make_command} is started")
                test_start = datetime.now()
                test_stdout, test_status_code = cls.run_test(test_path, make_command)
                cls.logger.info(f"Test result -\n{test_stdout}")
                test_end = datetime.now()
                parsed_test = SimxParser.parse_stdout(test_stdout)
                core_infos = [CoreInfo(
                    instructions=parsed_test.instructions[i],
                    cycles=parsed_test.cycles[i],
                    core=i
                ) for i in range(len(parsed_test.cycles) - 1)]
                test = Test(
                    elapsed_time=parsed_test.elapsed_time,
                    test_info=TestInfo(
                        file_path=FilePath(test_path),
                        make_command=MakeCommand(make_command)
                    ),
                    time_start=test_start,
                    time_end=test_end,
                    status=0 if test_status_code == 0 else 1,
                    cores_info=core_infos
                )
                tests.append(test)
                cls.logger.info(f"Run make command - {make_command} is ended")

            cls.logger.info(f"Processing test with test path - {test_path} is ended")
        tests_end = datetime.now()
        test_set = TestSet(
            time_start=tests_start,
            time_end=tests_end,
            tests=tests,
            tests_set_info=TestsSetInfo(
                vortex_commit_hash=cls.get_commit_hash_from_folder("./vortex"),
                commit_hash=cls.get_commit_hash_from_folder("."),
                toolchain_commit_hash=cls.get_toolchain_commit(),
                tests_set_params=TestsSetParams()
            )
        )
        cls.logger.info("Saving test set result")
        get_or_create_test_set(test_set)
        cls.vortex_stop()
        cls.logger.info("Testing is ended")

    @classmethod
    def create_test_sets_report(
            cls,
            report_folder: str,
            file_paths: Optional[List[str]] = None,
            l_bound: int = None,
            r_bound: int = None,
            tests_set_path: str = ""
    ):
        report_file_path = Visualizer.create_test_sets_report(find_test_sets(
            file_paths=file_paths,
            l_bound=l_bound,
            r_bound=r_bound,
            test_set_file_paths=cls.get_paths(tests_set_path) if tests_set_path else None
        ), report_folder)
        cls.logger.info(f"Report ({report_file_path}) is created")

    @classmethod
    def create_tests_report(
            cls,
            report_folder: str,
            file_paths: Optional[List[str]] = None,
            l_bound: int = None, r_bound: int = None,
            tests_set_path: str = ""
    ):
        report_file_path = Visualizer.create_tests_report(find_tests(
            file_paths=file_paths or [] + cls.get_paths(tests_set_path) if tests_set_path else [],
            l_bound=l_bound,
            r_bound=r_bound,
        ), report_folder)
        cls.logger.info(f"Report ({report_file_path}) is created")

    @classmethod
    def print_graphs(
            cls,
            test_ids: List[int],
            cycles: List[int], num_cores: List[int],
            elapsed_time: List[int],
            instrs: List[int]):
        plt.subplot(2, 2, 1)
        plt.xlabel('Test id')
        plt.ylabel('Cycles')
        plt.plot(test_ids, cycles)

        plt.subplot(2, 2, 2)
        plt.xlabel('Test id')
        plt.ylabel('Num cores')
        plt.plot(test_ids, num_cores)

        plt.subplot(2, 2, 3)
        plt.xlabel('Test id')
        plt.ylabel('Elapsed time')
        plt.plot(test_ids, elapsed_time)

        plt.subplot(2, 2, 4)
        ipc = [instar/cycle if cycle else 0 for cycle, instar in zip(cycles, instrs)]
        plt.xlabel('Test id')
        plt.ylabel('IPC')
        plt.plot(test_ids, ipc)
        plt.show()

    @classmethod
    def print_graphs_tests(
            cls,
            file_paths: Optional[List[str]] = None,
            l_bound: int = None,
            r_bound: int = None,
            tests_set_path: str = ""
    ):
        tests = find_tests(
            file_paths=file_paths or [] + cls.get_paths(tests_set_path) if tests_set_path else [],
            l_bound=l_bound,
            r_bound=r_bound
        )
        cycles = [sum(core_info.cycles for core_info in test.cores_info)
                  / len(test.cores_info) if test.cores_info else 0
                  for test in tests]
        num_cores = [len(test.cores_info) for test in tests]
        instrs = [sum(core_info.instructions for core_info in test.cores_info) for test in tests]
        test_ids = [test.id for test in tests]
        elapsed_time = [test.elapsed_time for test in tests]

        cls.print_graphs(test_ids, cycles, num_cores, elapsed_time, instrs)

    @classmethod
    def print_graphs_sets(
            cls,
            file_paths: Optional[List[str]] = None,
            l_bound: int = None,
            r_bound: int = None,
            tests_set_path: str = ""
    ):
        test_sets = find_test_sets(
            file_paths=file_paths,
            l_bound=l_bound,
            r_bound=r_bound,
            test_set_file_paths=cls.get_paths(tests_set_path) if tests_set_path else None
        )
        cycles_sum = [[test.cores_info[0].cycles for test in test_set.tests if test.cores_info] for test_set in test_sets]
        reference = cycles_sum[0]
        length = len(reference)
        cycles = [[tests[i]/reference[i] for i in range(length)] for tests in cycles_sum]
        cycles = [reduce(lambda a, b: a*b, tests)**(1/length) for tests in cycles]
        test_set_ids = [test_set.id for test_set in test_sets]
        plt.xlabel('Tests set id')
        plt.ylabel("Geom")
        plt.plot(test_set_ids, cycles)
        plt.show()

