from datetime import datetime as dt
from anthill.signal_handler import Run


def filter_runs(runs: list[Run], after: dt) -> list[Run]:
    filtered_runs = []
    for run in runs:
        if run.updated_at > after:
            filtered_runs.append(run)
    return filtered_runs


def sorter_runs(filtered_runs: list[Run], sort: str) -> list[Run]:
    return sorted(
        filtered_runs,
        key=lambda run: getattr(run, sort))
