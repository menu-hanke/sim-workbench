import builtins
from functools import cached_property
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from forestdatamodel.conversion.internal2mela import TreeSpecies
from app.app_io import export_cli_arguments
from app.file_io import pickle_reader, simulation_declaration_from_yaml_file
from sim.core_types import OperationPayload
import numpy as np
import numpy.typing as npt


Decl = Union[str, Dict[str,str], List["Decl"]]
CollectFn = Callable[[], float]


def compile(expr: str, globals: Dict) -> CollectFn:
    return eval(f"lambda: float({expr})", globals)


def _collect_fns(decl: Decl, globals: Dict, out: List[CollectFn]):
    if isinstance(decl, str):
        out.append(compile(decl, globals))
    elif isinstance(decl, dict):
        for k,v in decl.items():
            fn = compile(v, globals)
            fn.name = k
            out.append(fn)
    else:
        for x in decl:
            _collect_fns(x, globals, out)


class CollectFns(dict):

    def __init__(self, decl: Decl):
        self._fns: List[CollectFn] = []
        self._globals: Optional[Globals] = None
        _collect_fns(decl, self, self._fns)

    def __missing__(self, name: str) -> Any:
        return getattr(self._globals, name)

    def __call__(self, payload: OperationPayload) -> Iterator[float]:
        self._globals = Globals(payload)
        for f in self._fns:
            v = f()
            if hasattr(f, "name"):
                setattr(self._globals, f.name, v)
            yield v

    @cached_property
    def names(self) -> List[Optional[str]]:
        return [getattr(f, "name", None) for f in self._fns]


class CollectibleNDArray(np.ndarray):
    def __float__(self) -> float:
        return float(sum(self))


class LazyDataFrame:

    def __init__(self, xs: List):
        self._xs = xs

    def __getattr__(self, attr: str) -> npt.NDArray:
        arr = np.array([getattr(x, attr) for x in self._xs]).view(CollectibleNDArray)
        setattr(self, attr, arr)
        return arr


class Globals:

    def __init__(self, payload: OperationPayload):
        self._payload = payload

    def __getattr__(self, name: str) -> Any:
        try:
            return getattr(self._payload, name)
        except AttributeError:
            pass
        try:
            return getattr(TreeSpecies, name)
        except AttributeError:
            pass
        return getattr(builtins, name)

    @cached_property
    def trees(self):
        return LazyDataFrame(self._payload.simulation_state.reference_trees)

    @cached_property
    def strata(self):
        return LazyDataFrame(self._payload.simulation_state.tree_strata)


def export_j(decl: Dict, data: Dict[str, List[OperationPayload]]):
    xfns = CollectFns(decl.get("xvariables", []))
    cfns = CollectFns(decl.get("cvariables", []))
    xdaout = open(decl.get("xda", "data.xda"), "w")
    cdaout = open(decl.get("cda", "data.cda"), "w")
    if all(name is not None for name in xfns.names):
        xdaout.write(", ".join(xfns.names)) # type: ignore
        xdaout.write("\n")
    if all(name is not None for name in cfns.names):
        cdaout.write(", ".join(["ns", *cfns.names])) # type: ignore
        cdaout.write("\n")
    for schedules in data.values():
        if not schedules:
            continue
        cdaout.write("\t".join(map(str, [len(schedules), *cfns(schedules[0])])))
        cdaout.write("\n")
        for sched in schedules:
            xdaout.write("\t".join(map(str, xfns(sched))))
            xdaout.write("\n")
    xdaout.close()
    cdaout.close()


def main():
    args = export_cli_arguments(sys.argv[1:])
    data = pickle_reader(args.input_file)
    decl = simulation_declaration_from_yaml_file(args.control_file)
    format = decl.get("format", "j").lower()
    if format == "j":
        export_j(decl, data)
    else:
        raise ValueError("Unknown output format: '{}'".format(format))

if __name__ == "__main__":
    main()
