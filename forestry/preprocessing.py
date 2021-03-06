from typing import List
from forestdatamodel.model import ForestStand

def exclude_sapling_trees(stands: List[ForestStand], **operation_params) -> List[ForestStand]:
    for stand in stands:
        stand.reference_trees = list(filter(lambda t: (t if t.sapling is False else None), stand.reference_trees))
    return stands

def exclude_empty_stands(stands: List[ForestStand], **operation_params)-> List[ForestStand]:
    stands = list(filter(lambda s: (s if len(s.reference_trees) > 0 else None), stands))
    return stands

def exclude_zero_stem_trees(stands: List[ForestStand], **operation_params) -> List[ForestStand]:
    for stand in stands:
        stand.reference_trees = list(filter(lambda rt: rt.stems_per_ha > 0.0, stand.reference_trees))
    return stands

def compute_location_metadata(stands: List[ForestStand], **operation_params) -> List[ForestStand]:
    """
    This operation sets in-place the location based metadata properties for each given ForestStand, where missing.
    These properties are: height above sea level, temperature sum, sea effect, lake effect, monthly temperature and
    monthly rainfall
    """
    # import constrained to here as pymotti is an optional dependency
    from pymotti.lasum import ilmanor
    from pymotti.coord import etrs_tm35_to_ykj as conv
    from pymotti.kor import xkor

    for stand in stands:
        if stand.geo_location[3] == 'EPSG:3067':
            lat, lon = conv(stand.geo_location[0] / 1000, stand.geo_location[1] / 1000)
        elif stand.geo_location[3] == 'EPSG:2393':
            lat, lon = (stand.geo_location[0] / 1000, stand.geo_location[1] / 1000)
        else:
            raise Exception("Unsupported CRS {} for stand {}".format(stand.geo_location[3], stand.identifier))

        if stand.geo_location[2] is None:
            stand.geo_location = (
                stand.geo_location[0],
                stand.geo_location[1],
                xkor(lat, lon),
                stand.geo_location[3]
            )
        wi = ilmanor(lon, lat, stand.geo_location[2])

        if stand.degree_days is None:
            stand.degree_days = wi.dd
        if stand.sea_effect is None:
            stand.sea_effect = wi.sea
        if stand.lake_effect is None:
            stand.lake_effect = wi.lake
        if stand.monthly_temperatures is None:
            stand.monthly_temperatures = wi.temp
        if stand.monthly_rainfall is None:
            stand.monthly_rainfall = wi.rain
    return stands

operation_lookup = {
    'exclude_sapling_trees': exclude_sapling_trees,
    'exclude_empty_stands': exclude_empty_stands,
    'exclude_zero_stem_trees': exclude_zero_stem_trees,
    'compute_location_metadata': compute_location_metadata
}
