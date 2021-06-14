from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from .core_info import CoreInfo
from .test_info import TestInfo


@dataclass
class Test:

    time_start: datetime
    time_end: datetime
    status: int
    test_info: TestInfo
    cores_info: List[CoreInfo]
    elapsed_time: int
    id: Optional[int] = None
