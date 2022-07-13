from typing import Tuple, List
from forestryfunctions.naturalprocess.grow_acta import grow_diameter_and_height, grow_saplings
from forestdatamodel.model import ForestStand, ReferenceTree

def split_sapling_trees(trees: List[ReferenceTree]) -> Tuple[List[ReferenceTree], List[ReferenceTree]]:
    saplings, matures = [], []
    for tree in trees:
        saplings.append(tree) if tree.sapling is True else matures.append(tree)
    return saplings, matures


def grow_acta(input: Tuple[ForestStand, None], **operation_parameters) -> Tuple[ForestStand, None]:
    # TODO: Source years from simulator configurations
    stand, _ = input
    if len(stand.reference_trees) == 0:
        return input
    saplings, matures = split_sapling_trees(stand.reference_trees)
    grow_saplings(saplings)
    grow_diameter_and_height(matures)
    return stand, None
