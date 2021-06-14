from app.arg_parser import get_args
from app.command_executer import CommandExecuter
from app.logger import get_logger

logger = get_logger()


def execute_console_commands() -> None:
    _args = get_args()
    if getattr(_args, "toolchain_command", None):
        if _args.toolchain_command == "build":
            CommandExecuter.toolchain_build(_args.docker_folder, _args.docker_context)
    if getattr(_args, "vortex_command", None):
        if _args.vortex_command == "build":
            CommandExecuter.vortex_build(_args.docker_folder,
                                         _args.docker_context,
                                         _args.docker_compose_file)
        if _args.vortex_command == "migrate":
            CommandExecuter.migrate()
        if _args.vortex_command == "start":
            CommandExecuter.vortex_start()
        if _args.vortex_command == "stop":
            CommandExecuter.vortex_stop()
    if getattr(_args, "tests_command", None):
        if _args.tests_command == "run":
            CommandExecuter.vortex_run_tests(_args.tests_set_path)
    if getattr(_args, "git_command", None):
        if _args.git_command == "update_submodules":
            CommandExecuter.update_submodules()
    if getattr(_args, "visualizer_command", None):
        if _args.visualizer_command == "report_sets":
            CommandExecuter.create_test_sets_report(
                _args.report_folder,
                file_paths=_args.file_paths,
                l_bound=_args.l_bound,
                r_bound=_args.r_bound,
                tests_set_path=_args.tests_set_path
            )
        if _args.visualizer_command == "report_tests":
            CommandExecuter.create_tests_report(
                _args.report_folder,
                file_paths=_args.file_paths,
                l_bound=_args.l_bound,
                r_bound=_args.r_bound,
                tests_set_path=_args.tests_set_path
            )
        if _args.visualizer_command == "print_tests":
            CommandExecuter.print_graphs_tests(
                file_paths=_args.file_paths,
                l_bound=_args.l_bound,
                r_bound=_args.r_bound,
                tests_set_path=_args.tests_set_path
            )
        if _args.visualizer_command == "print_sets":
            if not _args.tests_set_path:
                logger.error("--print-sets attribute is required")
            CommandExecuter.print_graphs_sets(
                file_paths=_args.file_paths,
                l_bound=_args.l_bound,
                r_bound=_args.r_bound,
                tests_set_path=_args.tests_set_path
            )


def main():
    execute_console_commands()


if __name__ == "__main__":
    main()
