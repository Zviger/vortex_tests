from re import findall

from .interface import Parser
from app.entities import ParsedData


class SimxParser(Parser):

    @staticmethod
    def parse_stdout(stdout: str) -> ParsedData:
        instructions = list(map(int, findall(r"instrs=(\d+)", stdout)))
        cycles = list(map(int, findall(r"cycles=(\d+)", stdout)))
        elapsed_time = findall(r"Elapsed time: (\d+)", stdout)
        elapsed_time = int(elapsed_time[0]) if elapsed_time else -1
        return ParsedData(
            instructions=instructions,
            cycles=cycles,
            elapsed_time=elapsed_time
        )
