import argparse
from argparse import Namespace


def get_args() -> Namespace:
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers()

    toolchain_sub_parser = sub_parser.add_parser("toolchain")
    toolchain_sub_parser.add_argument("toolchain_command", metavar="command",
                                      help="Toolchain commands", choices=["build"])
    toolchain_build_group = toolchain_sub_parser.add_argument_group("Build")
    toolchain_build_group.add_argument("--docker-folder", dest="docker_folder",
                                       help="Toolchain Dockerfile's folder location",
                                       default="./docker")
    toolchain_build_group.add_argument("--context", dest="docker_context",
                                       help="Toolchain docker context location", default=".")

    vortex_sub_parser = sub_parser.add_parser("vortex")
    vortex_sub_parser.add_argument("vortex_command",
                                   metavar="command",
                                   help="Vortex commands: build, migrate, start, stop, run_tests",
                                   choices=["build", "migrate", "start", "stop", "run_tests"])
    vortex_build_group = vortex_sub_parser.add_argument_group("Build")
    vortex_build_group.add_argument("--docker-folder", dest="docker_folder",
                                    help="Dockerfile's folder location",
                                    default="./docker")
    vortex_build_group.add_argument("--context", dest="docker_context",
                                    help="Docker's context location", default=".")
    vortex_build_group.add_argument("--docker-compose-file", dest="docker_compose_file",
                                    help="Docker-compose file location",
                                    default="./docker-compose.yaml")

    tests_sub_parser = sub_parser.add_parser("tests")
    tests_sub_parser.add_argument("tests_command", metavar="command",
                                  help="Toolchain commands", choices=["run"])
    tests_run_group = tests_sub_parser.add_argument_group("Run tests")
    tests_run_group.add_argument("--tests-set", dest="tests_set_path",
                                 help="Location of file with tests paths",
                                 default="./test_sets/default.json")

    visualizer_sub_parser = sub_parser.add_parser("visualizer")
    visualizer_sub_parser.add_argument(
        "visualizer_command", metavar="command",
        help="Visualizer commands (report_sets, report_tests, print_tests, print_sets)",
        choices=["report_sets",
                 "report_tests",
                 "print_tests",
                 "print_sets"])
    visualizer_sub_parser.add_argument("--report-folder", dest="report_folder",
                                       help="Path to report's folder",
                                       default="./reports")
    visualizer_sub_parser.add_argument("--file-paths", dest="file_paths",
                                       help="File paths contains",
                                       default=[], nargs="*")
    visualizer_sub_parser.add_argument("--l-bound", dest="l_bound",
                                       help="Left bound of result",
                                       default=None, type=int, )
    visualizer_sub_parser.add_argument("--r-bound", dest="r_bound",
                                       help="Right bound of result",
                                       default=None, type=int)
    visualizer_sub_parser.add_argument("--tests-set", dest="tests_set_path",
                                       help="Location of file with tests paths")

    git_sub_parser = sub_parser.add_parser("git")
    git_sub_parser.add_argument("git_command", metavar="command",
                                help="Git commands", choices=["update_submodules"])

    return parser.parse_args()
