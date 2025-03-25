from datetime import datetime as dt
from typing import List
from anthill.signal_handler import Run


def filter_runs(runs: List[Run], after: dt) -> List[Run]:
    filtered_runs = []
    for run in runs:
        if run.updated_at > after:
            filtered_runs.append(run)
    return filtered_runs


def sorter_runs(filtered_runs: List[Run], sort: str) -> List[Run]:
    return sorted(
        filtered_runs,
        key=lambda run: getattr(run, sort))
