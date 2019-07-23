import numpy as np
import pandas as pd
import gdal
# from .read_data import ad_industrial_database_dict
# from .read_data import ad_industry_profiles_dict
# from .read_data import ad_residential_heating_profile_dict
from .read_data import ad_industry_profiles_local, ad_residential_heating_profile_local, ad_tertiary_profile_local, raster_array, ad_nuts_id, ad_industrial_database_local
from .CM1 import create_normalized_profiles


np.seterr(divide='ignore', invalid='ignore')

def get_value_at_point(arr, gt, pos):
  x = int((pos[0] - gt[0])/gt[1])
  y = int((pos[1] - gt[3])/gt[5])
  return arr[y, x]

def load_profile_gen(res_heating_share, industry_share, tertiary_share, nuts2_ids, heat_density_raster_total, heat_density_raster_res, heat_density_raster_nonres, gfa_res_curr_density, gfa_nonres_curr_density, nuts_id_number, output_directory):

    industrial_subsector_map = {"Iron and steel": "iron_and_steel", "Refineries": "chemicals_and_petrochemicals",
                                "Chemical industry": "chemicals_and_petrochemicals", "Cement": "non_metalic_minerals",
                                "Glass": "non_metalic_minerals",
                                "Non-metallic mineral products": "non_metalic_minerals", "Paper and printing": "paper",
                                "Non-ferrous metals": "iron_and_steel", "Other non-classified": "food_and_tobacco"}

    nuts0_ids = []
    for id_ in nuts2_ids:
        nuts0_ids.append(id_[:2])

    heat_sources = ad_industrial_database_local(nuts2_ids)
    # load heating profiles for sources and sinks
    # industry_profiles = ad_industry_profiles_dict(source_profiles)
    # residential_heating_profile = ad_residential_heating_profile_dict(sink_profiles)
    industry_profiles = ad_industry_profiles_local(nuts0_ids)
    residential_heating_profile = ad_residential_heating_profile_local(nuts2_ids)
    tertiary_profiles = ad_tertiary_profile_local(nuts2_ids)

    # kWh/m^2/a
    warm_water_density_res = {"AT": 21.67, "BE": 31.95, "BG": 12.93, "HR": 21.38, "CY": 8.80, "CZ": 22.83, "DK": 9.64,
                              "EE": 14.35, "FI": 10.15, "FR": 9.66, "DE": 8.27, "EL": 12.51, "HU": 13.66, "IE": 15.91,
                              "IT": 14.01, "LV": 15.71, "LT": 13.36, "LU": 8.29, "MT": 10.99, "NL": 8.91, "PL": 10.00,
                              "PT": 9.48, "RO": 11.48, "SK": 21.51, "SI": 21.74, "ES": 23.34, "SE": 13.54, "UK": 49.03}
    warm_water_density_ter = {"AT": 6.57, "BE": 13.88, "BG": 15.88, "HR": 9.42, "CY": 6.26, "CZ": 9.18, "DK": 8.03,
                              "EE": 14.13, "FI": 10.52, "FR": 9.57, "DE": 3.05, "EL": 6.99, "HU": 9.51, "IE": 10.87,
                              "IT": 5.62, "LV": 7.16, "LT": 10.46, "LU": 7.2, "MT": 10.45, "NL": 6.89, "PL": 9.55,
                              "PT": 21.47, "RO": 13.85, "SK": 8.49, "SI": 27.73, "ES": 12.44, "SE": 19.62, "UK": 13.45}

    if isinstance(heat_density_raster_total, np.ndarray):
        hdm_arr_total = heat_density_raster_total
    else:
        hdm_arr_total, gt_total = raster_array(heat_density_raster_total, return_gt=True)

    if isinstance(heat_density_raster_res, np.ndarray):
        hdm_arr_res = heat_density_raster_res
    else:
        hdm_arr_res, gt_res = raster_array(heat_density_raster_res, return_gt=True)

    if isinstance(heat_density_raster_nonres, np.ndarray):
        hdm_arr_nonres = heat_density_raster_nonres
    else:
        hdm_arr_nonres, gt_nonres = raster_array(heat_density_raster_nonres, return_gt=True)

    if isinstance(gfa_res_curr_density, np.ndarray):
        gfa_res_arr = gfa_res_curr_density
    else:
        gfa_res_arr, gt_fra_res = raster_array(gfa_res_curr_density, return_gt=True)

    if isinstance(gfa_nonres_curr_density, np.ndarray):
        gfa_nonres_arr = gfa_nonres_curr_density
    else:
        gfa_nonres_arr, gt_fra_nonres = raster_array(gfa_nonres_curr_density, return_gt=True)

    if isinstance(nuts_id_number, np.ndarray):
        nuts_id_number = heat_density_raster_nonres
    else:
        nuts_id_number, gt_nuts = raster_array(nuts_id_number, return_gt=True)

    nuts_id_map = ad_nuts_id()

    id = get_value_at_point(nuts_id_number, gt_nuts, (4968964.4, 3121416.0))
    nuts = nuts_id_map[nuts_id_map["id"] == id].values[0][1]

    nuts_ids = np.unique(nuts_id_number)
    total_heat_per_nuts = []
    res_heat_per_nuts = []
    nonres_heat_per_nuts = []
    gfa_res_per_nuts = []
    gfa_nonres_per_nuts = []
    surface_area_per_nuts = []
    nuts = []
    for nuts_id in nuts_ids:
        if nuts_id != 0:    # don't consider areas with no nuts id
            nuts2_id = nuts_id_map[nuts_id_map["id"] == nuts_id].values[0][1][0:4]
            if nuts2_id in nuts2_ids:   # check if load profile is available
                nuts.append(nuts2_id)
                ind = nuts_id_number == nuts_id
                surface_area_per_nuts.append(np.sum(ind)*0.01)  # each tile is 0.01 km^2
                total_heat_per_nuts.append(np.sum(hdm_arr_total[ind]))   # GWh
                res_heat_per_nuts.append(np.sum(hdm_arr_res[ind]))   # GWh
                nonres_heat_per_nuts.append(np.sum(hdm_arr_nonres[ind]))   # GWh
                gfa_res_per_nuts.append(np.sum(gfa_res_arr[ind]))   # m^2
                gfa_nonres_per_nuts.append(np.sum(gfa_nonres_arr[ind]))     # m^2

    # normalize loaded profiles
    normalized_heat_profiles = dict()
    normalized_heat_profiles["residential_heating"] = create_normalized_profiles(residential_heating_profile[0],
                                                                                 "NUTS2_code", "hour", "load")
    normalized_heat_profiles["sanitary_hot_water_residential"] = create_normalized_profiles(residential_heating_profile[1],
                                                                                            "NUTS2_code", "hour", "load")
    normalized_heat_profiles["Sanitary Hot Water Tertiary"] = create_normalized_profiles(tertiary_profiles[0],
                                                                                         "NUTS2_code", "hour", "load")
    normalized_heat_profiles["Heating Tertiary"] = create_normalized_profiles(tertiary_profiles[1],
                                                                              "NUTS2_code", "hour", "load")

    for industry_profile in industry_profiles:
        normalized_heat_profiles[industry_profile.iloc[1]["process"]] = \
            create_normalized_profiles(industry_profile, "NUTS0_code", "hour", "load")

    # drop all sinks with unknown or invalid nuts id
    heat_sources = heat_sources[heat_sources.Nuts0_ID != ""]
    heat_sources = heat_sources.dropna()
    for sub_sector in industrial_subsector_map:
        missing_profiles = list(set(heat_sources[heat_sources.Subsector == sub_sector]["Nuts0_ID"].unique()) -
                                set(normalized_heat_profiles[industrial_subsector_map[sub_sector]].keys()))
        for missing_profile in missing_profiles:
            heat_sources = heat_sources[((heat_sources.Nuts0_ID != missing_profile) |
                                         (heat_sources.Subsector != sub_sector))]

    # compute profiles
    heat_source_profiles = []
    for _, heat_source in heat_sources.iterrows():
        heat_source_profiles.append(normalized_heat_profiles[
            industrial_subsector_map[heat_source["Subsector"]]][heat_source["Nuts0_ID"]] * float(heat_source["Excess_heat"]))
    heat_source_profiles = np.array(heat_source_profiles)
    industry_profile = np.sum(heat_source_profiles, axis=0)

    res_heating_profile = np.zeros(8760)
    res_shw_profile = np.zeros(8760)
    ter_heating_profile = np.zeros(8760)
    ter_shw_profile = np.zeros(8760)
    for nuts_id, res_heat, surface, gfa_res in zip(nuts, res_heat_per_nuts, surface_area_per_nuts, gfa_res_per_nuts):
        res_heating_profile = res_heating_profile + normalized_heat_profiles["residential_heating"][nuts_id] *\
            (res_heat - gfa_res * warm_water_density_res[nuts_id[0:2]] / 1e3)
        res_shw_profile = res_shw_profile + normalized_heat_profiles["sanitary_hot_water_residential"][nuts_id] *\
            gfa_res * warm_water_density_res[nuts_id[0:2]] / 1e3

    for nuts_id, ter_heat, surface, gfa_nonres in zip(nuts, nonres_heat_per_nuts, surface_area_per_nuts, gfa_nonres_per_nuts):
        ter_heating_profile = ter_heating_profile + normalized_heat_profiles["residential_heating"][nuts_id] *\
            (ter_heat - gfa_nonres * warm_water_density_ter[nuts_id[0:2]] / 1e3)
        ter_shw_profile = ter_shw_profile + normalized_heat_profiles["sanitary_hot_water_residential"][nuts_id] *\
            gfa_nonres * warm_water_density_ter[nuts_id[0:2]] / 1e3

    effective_profile = industry_profile + res_heating_profile + res_shw_profile + ter_heating_profile + ter_shw_profile

    data = np.array([[x for x in range(1, 8761)], effective_profile])
    data = data.transpose()
    data = pd.DataFrame(data, columns=["hour", "load"])
    data.to_csv(output_directory, index=False)

    industry_profile_monthly = np.mean(np.reshape(industry_profile, (12, 730)), axis=1).tolist()
    res_heating_profile_monthly = np.mean(np.reshape(res_heating_profile, (12, 730)), axis=1).tolist()
    res_shw_profile_monthly = np.mean(np.reshape(res_shw_profile, (12, 730)), axis=1).tolist()
    ter_heating_profile_monthly = np.mean(np.reshape(ter_heating_profile, (12, 730)), axis=1).tolist()
    ter_shw_profile_monthly = np.mean(np.reshape(ter_shw_profile, (12, 730)), axis=1).tolist()
    effective_profile_monthly = np.mean(np.reshape(effective_profile, (12, 730)), axis=1).tolist()

    return industry_profile_monthly, res_heating_profile_monthly, res_shw_profile_monthly, ter_heating_profile_monthly,\
        ter_shw_profile_monthly, effective_profile_monthly
