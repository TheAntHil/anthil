from datetime import datetime as dt
from typing import List
from anthill.signal_handler import Run


def filtering_runs(runs: List[Run], after: dt) -> List[Run]:
    filtered_runs = []
    for run in runs:
        if dt.fromisoformat(run.updated_at) > after:
            filtered_runs.append(run)
    return filtered_runs


def sorting_runs(filtered_runs: List[Run], sort: str) -> List[Run]:
    return sorted(
        filtered_runs,
        key=lambda run: dt.fromisoformat(getattr(run, sort)))


def run_filtering_sorting(runs: List[Run], after: dt, sort: str) -> List[Run]:
    filtered_runs = filtering_runs(runs, after)
    filtered_and_sorted_runs = sorting_runs(filtered_runs, sort)
    return filtered_and_sorted_runs
