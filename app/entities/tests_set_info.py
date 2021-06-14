from dataclasses import dataclass

from .commit_hash import CommitHash
from .tests_set_params import TestsSetParams


@dataclass
class TestsSetInfo:

    commit_hash: CommitHash
    vortex_commit_hash: CommitHash
    toolchain_commit_hash: CommitHash
    tests_set_params: TestsSetParams
