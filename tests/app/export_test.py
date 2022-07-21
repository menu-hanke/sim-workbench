import unittest
from forestdatamodel.enums.internal import TreeSpecies
from forestdatamodel.model import ForestStand, ReferenceTree
from app.export import CollectFns
from sim.core_types import OperationPayload


class TestExport(unittest.TestCase):
    def test_collect(self):
        collect = CollectFns([
            "simulation_state.year",
            "trees.stems_per_ha[trees.species==1]"
        ])
        payload = OperationPayload()
        payload.simulation_state = ForestStand(
            year = 2022,
            reference_trees = [
                ReferenceTree(stems_per_ha=10, species=TreeSpecies.PINE),
                ReferenceTree(stems_per_ha=20, species=TreeSpecies.SPRUCE),
                ReferenceTree(stems_per_ha=40, species=TreeSpecies.PINE)
            ]
        )
        values = list(collect(payload))
        self.assertEqual(values, [2022, 50])
