from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from .tests_set_info import TestsSetInfo
from .test import Test


@dataclass
class TestSet:

    time_start: datetime
    time_end: datetime
    tests_set_info: TestsSetInfo
    tests: List[Test]
    id: Optional[int] = None
