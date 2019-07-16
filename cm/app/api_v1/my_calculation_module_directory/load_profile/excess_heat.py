import numpy as np
import pandas as pd
# from .read_data import ad_industrial_database_dict
# from .read_data import ad_industry_profiles_dict
# from .read_data import ad_residential_heating_profile_dict
from .read_data import ad_industry_profiles_local, ad_residential_heating_profile_local, ad_tertiary_profile_local
from .CM1 import create_normalized_profiles


np.seterr(divide='ignore', invalid='ignore')


def load_profile_gen(res_heating_share, industry_share, tertiary_share, nuts2_ids, output_directory):

    industrial_subsector_map = {"Iron and steel": "iron_and_steel", "Refineries": "chemicals_and_petrochemicals",
                                "Chemical industry": "chemicals_and_petrochemicals", "Cement": "non_metalic_minerals",
                                "Glass": "non_metalic_minerals",
                                "Non-metallic mineral products": "non_metalic_minerals", "Paper and printing": "paper",
                                "Non-ferrous metals": "iron_and_steel", "Other non-classified": "food_and_tobacco"}

    nuts0_ids = []
    for id_ in nuts2_ids:
        nuts0_ids.append(id_[:2])

    # load heating profiles for sources and sinks
    # industry_profiles = ad_industry_profiles_dict(source_profiles)
    # residential_heating_profile = ad_residential_heating_profile_dict(sink_profiles)
    industry_profiles = ad_industry_profiles_local(nuts0_ids)
    residential_heating_profile = ad_residential_heating_profile_local(nuts2_ids)
    tertiary_profiles = ad_tertiary_profile_local(nuts2_ids)

    # normalize loaded profiles
    normalized_heat_profiles = dict()
    normalized_heat_profiles["residential_heating"] = create_normalized_profiles(residential_heating_profile,
                                                                                 "NUTS2_code", "hour", "load")
    normalized_heat_profiles["Sanitary Hot Water Tertiary"] = create_normalized_profiles(tertiary_profiles,
                                                                                         "NUTS2_code", "hour", "load")

    for industry_profile in industry_profiles:
        normalized_heat_profiles[industry_profile.iloc[1]["process"]] = \
            create_normalized_profiles(industry_profile, "NUTS0_code", "hour", "load")

    industry_profile = np.zeros(8760)
    for nuts0_id in nuts0_ids:
        for subsector in industrial_subsector_map.values():
            industry_profile = industry_profile + normalized_heat_profiles[subsector][nuts0_id]

    industry_profile = industry_profile / np.sum(industry_profile)

    res_heating_profile = np.zeros(8760)
    tertiary_profile = np.zeros(8760)
    for nuts2_id in nuts2_ids:
        res_heating_profile = res_heating_profile + normalized_heat_profiles["residential_heating"][nuts2_id]
        tertiary_profile = tertiary_profile + normalized_heat_profiles["Sanitary Hot Water Tertiary"][nuts2_id]

    res_heating_profile = res_heating_profile / np.sum(res_heating_profile)
    tertiary_profile = tertiary_profile / np.sum(tertiary_profile)

    effective_profile = res_heating_share * res_heating_profile + industry_share * industry_profile + \
        tertiary_share * tertiary_profile

    effective_profile = effective_profile / np.sum(effective_profile)

    data = np.array([[x for x in range(1, 8761)], effective_profile])
    data = data.transpose()

    data = pd.DataFrame(data, columns=["hour", "load"])

    industry_profile_monthly = np.sum(np.reshape(industry_profile, (12, 730)), axis=1).tolist()
    residential_heating_profile_monthly = np.sum(np.reshape(res_heating_profile, (12, 730)), axis=1).tolist()
    tertiary_profile_monthly = np.sum(np.reshape(tertiary_profile, (12, 730)), axis=1).tolist()
    effective_profile_monthly = np.sum(np.reshape(effective_profile, (12, 730)), axis=1).tolist()

    data.to_csv(output_directory, index=False)

    return industry_profile_monthly, residential_heating_profile_monthly, tertiary_profile_monthly,\
        effective_profile_monthly






