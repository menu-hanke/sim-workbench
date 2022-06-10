from typing import List
from forestdatamodel.model import ForestStand

def exclude_sapling_trees(stands: List[ForestStand], **operation_params) -> List[ForestStand]:
    for stand in stands:
        #is there benefit from using filter here since it returns a generator which should be read from straight away? 
        stand.reference_trees = list(filter(lambda t: (t if t.sapling is False else None), stand.reference_trees))
    return stands

def exclude_empty_stands(stands: List[ForestStand], **operation_params)-> List[ForestStand]:
    #is there benefit from using filter here since it returns a generator which should be read from straight away? 
    stands = list(filter(lambda s: (s if len(s.reference_trees) > 0 else None), stands))
    return stands

operation_lookup = {
    'exclude_sapling_trees': exclude_sapling_trees,
    'exclude_empty_stands': exclude_empty_stands
}