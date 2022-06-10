"""
This module contains a collection of util functions and dummy payload functions for test cases
"""
import os
import unittest
from typing import Any, List, Optional, Tuple, Callable
from forestry.aggregate_utils import get_latest_operation_aggregate, store_operation_aggregate

import yaml

from sim.core_types import OperationPayload


class ConverterTestSuite(unittest.TestCase):
    def run_with_test_assertions(self, assertions: List[Tuple], fn: Callable):
        for case in assertions:
            result = fn(*case[0])
            self.assertEqual(case[1], result)


def raises(x: Any) -> None:
    raise Exception("Run failure")


def identity(x: Any) -> Any:
    return x


def none(x: Any) -> None:
    return None


def aggregating_increment(input: Tuple[int, dict]) -> Tuple[int, dict]:
    state, aggregates = input
    latest_aggregate = get_latest_operation_aggregate(aggregates, 'aggregating_increment')
    aggregate = {'run_count': 1} if latest_aggregate is None else {'run_count': latest_aggregate['run_count'] + 1}
    new_aggregates = store_operation_aggregate(aggregates, aggregate, 'aggregating_increment')
    return state + 1, new_aggregates


def inc(x: int) -> int:
    return x + 1


def dec(x: int) -> int:
    return x - 1


def max_reducer(x: List[int]) -> Optional[int]:
    return max(x)


def parametrized_operation(x, **kwargs):
    if kwargs.get('amplify') is True:
        return x * 1000
    else:
        return x


def collect_results(payloads: List[OperationPayload]) -> List:
    return list(map(lambda payload: payload.simulation_state, payloads))


def file_contents(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


def load_yaml(file_name: str) -> dict:
    return yaml.load(file_contents(os.path.join(os.getcwd(), "tests", "resources", file_name)), Loader=yaml.CLoader)
