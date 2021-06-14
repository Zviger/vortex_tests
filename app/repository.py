from typing import List, Optional

from .entities import (TestSet, CommitHash, TestsSetParams, TestsSetInfo,
                       CoreInfo, FilePath, Test, TestInfo, MakeCommand)
from .logger import get_logger
from .models import (TestSetModel, TestInfoModel, TestsSetInfoModel,
                     CommitHashModel, TestsSetParamsModel, CoreInfoModel,
                     FilePathModel, TestModel, MakeCommandModel)
from .database import db

logger = get_logger()


def get_or_create_test_set(test_set_entity: TestSet) -> TestSetModel:
    with db.atomic():
        test_set, _ = TestSetModel.get_or_create(
            time_start=test_set_entity.time_start,
            time_end=test_set_entity.time_end,
            tests_set_info_id=get_or_create_tests_set_info(test_set_entity.tests_set_info)
        )
    for test in test_set_entity.tests:
        get_or_create_test(test, test_set)
    return test_set


def get_or_create_commit_hash(commit_hash_entity: CommitHash) -> CommitHashModel:
    with db.atomic():
        commit_hash, _ = CommitHashModel.get_or_create(
            hash=commit_hash_entity.hash
        )
    return commit_hash


def get_or_create_tests_set_params(tests_set_params_entity: TestsSetParams) -> TestsSetParamsModel:
    with db.atomic():
        tests_set_params, _ = TestsSetParamsModel.get_or_create(

        )
    return tests_set_params


def get_or_create_tests_set_info(tests_set_info_entity: TestsSetInfo) -> TestsSetInfoModel:
    with db.atomic():
        test_set_info, _ = TestsSetInfoModel.get_or_create(
            commit_hash_id=get_or_create_commit_hash(tests_set_info_entity.commit_hash),
            vortex_commit_hash_id=get_or_create_commit_hash(tests_set_info_entity.vortex_commit_hash),
            toolchain_commit_hash_id=get_or_create_commit_hash(tests_set_info_entity.toolchain_commit_hash),
            tests_set_params_id=get_or_create_tests_set_params(tests_set_info_entity.tests_set_params)
        )
    return test_set_info


def get_or_create_cors_ticks(core_info_entity: CoreInfo, test_id: int) -> CoreInfoModel:
    with db.atomic():
        core_info, _ = CoreInfoModel.get_or_create(
            core=core_info_entity.core,
            cycles=core_info_entity.cycles,
            instructions=core_info_entity.instructions,
            test_id=test_id
        )
    return core_info


def get_or_create_file_path(file_path_entity: FilePath) -> FilePathModel:
    with db.atomic():
        file_path, _ = FilePathModel.get_or_create(
            path=file_path_entity.path
        )
    return file_path


def get_or_create_make_command(make_command_entity: MakeCommand) -> MakeCommandModel:
    with db.atomic():
        make_command, _ = MakeCommandModel.get_or_create(
            command=make_command_entity.command
        )
    return make_command


def get_or_create_test(test_entity: Test, test_set_id: int) -> TestModel:
    with db.atomic():
        test, _ = TestModel.get_or_create(
            time_start=test_entity.time_start,
            time_end=test_entity.time_end,
            status=test_entity.status,
            elapsed_time=test_entity.elapsed_time,
            test_info_id=get_or_create_test_info(test_entity.test_info),
            test_set_id=test_set_id
        )
    for core_info in test_entity.cores_info:
        get_or_create_cors_ticks(core_info, test)
    return test


def get_or_create_test_info(test_info_entity: TestInfo) -> TestInfoModel:
    with db.atomic():
        test_info, _ = TestInfoModel.get_or_create(
            file_path_id=get_or_create_file_path(test_info_entity.file_path),
            make_command_id=get_or_create_make_command(test_info_entity.make_command)
        )
    return test_info


def find_test_sets(
        file_paths: Optional[List[str]] = None,
        l_bound: int = None, r_bound: int = None,
        test_set_file_paths: Optional[List[str]] = None
) -> List[TestSet]:
    tests_set_models = (TestSetModel.select()
                        .join(TestsSetInfoModel, on=(TestsSetInfoModel.id == TestSetModel.tests_set_info_id))
                        .join(CommitHashModel, on=(TestsSetInfoModel.commit_hash_id == CommitHashModel.id |
                                                   TestsSetInfoModel.vortex_commit_hash_id == CommitHashModel.id |
                                                   TestsSetInfoModel.toolchain_commit_hash_id == CommitHashModel.id))
                        .join(TestsSetParamsModel, on=(TestsSetInfoModel.tests_set_params_id == TestsSetParamsModel.id))
                        .join(TestModel, on=(TestSetModel.id == TestModel.test_set_id))
                        .join(TestInfoModel)
                        .join(MakeCommandModel)
                        .join(FilePathModel, on=(TestInfoModel.file_path_id == FilePathModel.id))
                        .distinct()
                        )

    tests_set_models = sort_query(tests_set_models, file_paths)
    tests_set_models = list(tests_set_models)
    if test_set_file_paths:
        for tests_set_model in tests_set_models.copy():
            test_paths = [test.test_info.file_path.path for test in tests_set_model.tests]
            for test_path in test_set_file_paths:
                if test_path not in test_paths:
                    tests_set_models.remove(tests_set_model)
                    break
    test_sets = []
    length = len(tests_set_models)

    if l_bound:
        tests_set_models = tests_set_models[l_bound:]

    if r_bound:
        if r_bound > length:
            logger.error(f"r-bound can't be greater than {length}")
            exit(0)
        else:
            tests_set_models = tests_set_models[:r_bound]

    for tests_set_model in tests_set_models:
        test_set_info_model = tests_set_model.tests_set_info
        test_set_info = TestsSetInfo(
            commit_hash=CommitHash(test_set_info_model.commit_hash.hash),
            vortex_commit_hash=CommitHash(test_set_info_model.vortex_commit_hash.hash),
            toolchain_commit_hash=CommitHash(test_set_info_model.toolchain_commit_hash.hash),
            tests_set_params=TestsSetParams()
        )
        test_models = tests_set_model.tests
        test_set = TestSet(
            time_start=tests_set_model.time_start,
            time_end=tests_set_model.time_end,
            tests_set_info=test_set_info,
            tests=[get_test(test_model) for test_model in test_models],
            id=tests_set_model.id
        )
        test_sets.append(test_set)
    return test_sets


def get_test(test_model: TestModel) -> Test:
    test_info_model = test_model.test_info
    test = Test(
        test_info=TestInfo(
            make_command=test_info_model.make_command.command,
            file_path=test_info_model.file_path.path
        ),
        time_start=test_model.time_start,
        time_end=test_model.time_end,
        cores_info=[CoreInfo(
            instructions=core_info_model.instructions,
            cycles=core_info_model.cycles,
            core=core_info_model.core
        ) for core_info_model in test_model.core_infos],
        status=test_model.status,
        elapsed_time=test_model.elapsed_time,
        id=test_model.id
    )
    return test


def find_tests(file_paths: Optional[List[str]] = None, l_bound: int = None, r_bound: int = None) -> List[Test]:
    test_models = (TestModel.select()
                   .join(TestInfoModel)
                   .join(MakeCommandModel)
                   .join(FilePathModel, on=(TestInfoModel.file_path_id == FilePathModel.id))
                   )
    test_models = sort_query(test_models, file_paths)
    length = len(test_models)
    if l_bound:
        test_models = test_models[l_bound:]

    if r_bound:
        if r_bound > length:
            logger.error(f"r-bound can't be greater than {length}")
            exit(0)
        else:
            test_models = test_models[:r_bound]
    tests = [get_test(test_model) for test_model in test_models]
    return tests


def sort_query(
        query,
        file_paths: Optional[List[str]] = None,
):
    if file_paths:
        query = query.where(FilePathModel.path.in_(file_paths))

    return query
