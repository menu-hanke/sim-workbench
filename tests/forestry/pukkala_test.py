import unittest

from forestdatamodel.enums.internal import TreeSpecies
from forestdatamodel.model import ForestStand, ReferenceTree
import forestry.grow_pukkala_r


class RUtilsTest(unittest.TestCase):
    def test_pukkala_grow(self):
        fixture = ForestStand(
            degree_days=1234.0,
            geo_location=(6555234.0, 3290233, 79.0, "EPSG:3067"),
            site_type_category=1,
            soil_peatland_category=1
        )
        fixture.reference_trees = [
            ReferenceTree(
                identifier='tree-1',
                height=10.4,
                breast_height_diameter=20.3,
                species=TreeSpecies.PINE,
                biological_age=23.0,
                stems_per_ha=52.3),
            ReferenceTree(
                identifier='tree-2',
                height=13.4,
                breast_height_diameter=14.3,
                species=TreeSpecies.SILVER_BIRCH,
                biological_age=27.0,
                stems_per_ha=0)
        ]

        result = forestry.grow_pukkala_r.pukkala_growth(fixture)
        #result2 = forestry.grow_pukkala_r.pukkala_growth(result)
        #self.assertAlmostEqual(170.04, result, 2)
