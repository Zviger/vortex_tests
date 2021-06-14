from dataclasses import dataclass
from typing import List


@dataclass
class ParsedData:

    instructions: List[int]
    cycles: List[int]
    elapsed_time: int
