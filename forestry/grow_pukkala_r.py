from forestdatamodel.enums.internal import TreeSpecies
from forestdatamodel.model import ForestStand, ReferenceTree
from rpy2 import robjects as robjects


species_map: dict[TreeSpecies, int] = {
    TreeSpecies.PINE: 1,
    TreeSpecies.SPRUCE: 2,
    TreeSpecies.SILVER_BIRCH: 3,
    TreeSpecies.DOWNY_BIRCH: 4,
    TreeSpecies.POPLAR: 5,
    TreeSpecies.COMMON_ALDER: 6,
    TreeSpecies.UNKNOWN: 7
}

sitetype_map = {

}

pukkala_loaded = False

def pukkala_growth(stand: ForestStand) -> ForestStand:
    global pukkala_loaded
    if not pukkala_loaded:
        robjects.r.source('./r/pukkala_growth/growthfuncs.R')
        pukkala_loaded = True

    tree_data = {
        'id': robjects.IntVector([i for i, _ in enumerate(stand.reference_trees)]),
        'sp': robjects.IntVector([species_map.get(tree.species, 7) for tree in stand.reference_trees]),
        'dbh': robjects.FloatVector([tree.breast_height_diameter for tree in stand.reference_trees]),
        'Ntrees': robjects.FloatVector([tree.stems_per_ha for tree in stand.reference_trees]),
        'sitetype': robjects.IntVector([stand.site_type_category for _ in range(len(stand.reference_trees))]),
        'landclass': robjects.IntVector([stand.soil_peatland_category for _ in range(len(stand.reference_trees))]),
        'TS': robjects.FloatVector([stand.degree_days for _ in range(len(stand.reference_trees))]),
        'y': robjects.IntVector([stand.geo_location[0] for _ in range(len(stand.reference_trees))]),
        'x': robjects.IntVector([stand.geo_location[1] for _ in range(len(stand.reference_trees))]),
        'alt': robjects.FloatVector([stand.geo_location[2] for _ in range(len(stand.reference_trees))]),
        # TODO: harv needs sourcing from cutting history; 0: no operations within last 5 a, 1: yes
        'harv': robjects.IntVector([0 for _ in range(len(stand.reference_trees))]),
        'yr': robjects.IntVector([tree.biological_age for tree in stand.reference_trees])
    }
    dtin = robjects.DataFrame(tree_data)
    results = list(robjects.r['grow'](dtin, path="./r/pukkala_growth/", standArea=stand.area))

    for i in range(len(results[0])):
        existing_count = len(stand.reference_trees)
        if i < existing_count:
            tree = stand.reference_trees[i]
            tree.breast_height_diameter = results[2][i]
            tree.stems_per_ha = results[3][i]
            tree.biological_age = results[11][i]
        else:
            stand.reference_trees.append(ReferenceTree(
                identifier=str(results[0][i]),
                species={value: key for key, value in species_map.items()}[results[1][i]],
                breast_height_diameter=results[2][i],
                stems_per_ha=results[3][i],
                biological_age=results[11][i]
            ))

    return stand

# R script initialization, library deps
# VGAM needed?
# id missing -> str
# geocoordinate CRS -> YKJ, Lauri tarkistaa CRS:n
# yr value -> biological_age ok, increased
# result ordering guarantee -> yes
# remove trees with stems_per_ha < 0.01
