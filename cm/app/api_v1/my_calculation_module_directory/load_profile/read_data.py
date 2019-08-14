import pandas as pd
import os
import csv
import gdal
import numpy as np
import re




def ad_industry_profiles_dict(dicts):
    dict_names = ["load_profile_industry_chemicals_and_petrochemicals_yearlong_2018",
                  "load_profile_industry_food_and_tobacco_yearlong_2018",
                  "load_profile_industry_iron_and_steel_yearlong_2018",
                  "load_profile_industry_non_metalic_minerals_yearlong_2018",
                  "load_profile_industry_paper_yearlong_2018"]
    data = []
    for name, dictionary in zip(dict_names, dicts):
        raw_data = pd.DataFrame(dictionary[name])
        raw_data = raw_data.loc[:, ("NUTS0_code", "process", "hour", "load")]
        raw_data["load"] = pd.to_numeric(raw_data["load"])
        raw_data["hour"] = pd.to_numeric(raw_data["hour"])
        data.append(raw_data)

    return data


def ad_residential_heating_profile_dict(dictionary):

    data = pd.DataFrame(dictionary["load_profile_residential_heating_yearlong_2010"])
    data = data.loc[:, ("NUTS2_code", "process", "hour", "load")]
    data["load"] = pd.to_numeric(data["load"])
    data["hour"] = pd.to_numeric(data["hour"])
    return data


def ad_industry_profiles_local(nuts0_ids):
    """
    Loads industry profiles of different subcategories from different csv files.

    :return: List of dataframes containing the csv files data.
    :rtype: list [pd.Dataframe, pd.Dataframe, ...].
    """

    file_names = ("hotmaps_task_2.7_load_profile_industry_chemicals_and_petrochemicals_yearlong_2018.csv",
                  "hotmaps_task_2.7_load_profile_industry_food_and_tobacco_yearlong_2018.csv",
                  "hotmaps_task_2.7_load_profile_industry_iron_and_steel_yearlong_2018.csv",
                  "hotmaps_task_2.7_load_profile_industry_non_metalic_minerals_yearlong_2018.csv",
                  "hotmaps_task_2.7_load_profile_industry_paper_yearlong_2018.csv")

    path = os.path.dirname(
           os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "data")

    data = []
    for file_name in file_names:
        sub_path = os.path.join(path, file_name)
        # determine delimiter of csv file
        with open(sub_path, 'r', encoding='utf-8') as csv_file:
            delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter

        raw_data = pd.read_csv(sub_path, sep=delimiter, usecols=("NUTS0_code", "process", "hour", "load"))
        raw_data = raw_data[raw_data["NUTS0_code"].isin(nuts0_ids)]
        data.append(raw_data)

    return data


def ad_residential_heating_profile_local(nuts2_ids):
    """
    Loads residential heating profiles from csv file.

    :return: Dataframe containing the data of the csv file.
    :rtype: pandas dataframe.
    """

    path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "data")
    path1 = os.path.join(path, "hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010_part1.csv")
    path2 = os.path.join(path, "hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010_part2.csv")
    path3 = os.path.join(path, "data_hotmaps_task_2.7_load_profile_residential_shw_yearlong_2010_part1.csv")
    path4 = os.path.join(path, "data_hotmaps_task_2.7_load_profile_residential_shw_yearlong_2010_part2.csv")
    paths = [path1, path2]
    # determine delimiter of csv file
    data = pd.DataFrame(columns=("NUTS2_code", "process", "hour", "load"))
    for path in paths:
        with open(path, 'r', encoding='utf-8') as csv_file:
            delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
        dat = pd.read_csv(path, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
        data = data.append(dat)
    data = data[data["NUTS2_code"].isin(nuts2_ids)]

    paths = [path3, path4]
    data2 = pd.DataFrame(columns=("NUTS2_code", "process", "hour", "load"))
    for path in paths:
        with open(path, 'r', encoding='utf-8') as csv_file:
            delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
        dat = pd.read_csv(path, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
        data2 = data2.append(dat)
    data2 = data2[data2["NUTS2_code"].isin(nuts2_ids)]

    return data, data2


def ad_tertiary_profile_local(nuts2_ids):
    """
    Loads residential heating profiles from csv file.

    :return: Dataframe containing the data of the csv file.
    :rtype: pandas dataframe.
    """

    path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "data")
    path1 = os.path.join(path, "data_hotmaps_task_2.7_load_profile_tertiary_heating_yearlong_2010_part1.csv")
    path2 = os.path.join(path, "data_hotmaps_task_2.7_load_profile_tertiary_heating_yearlong_2010_part2.csv")
    path3 = os.path.join(path, "hotmaps_task_2.7_load_profile_tertiary_shw_yearlong_2010_part1.csv")
    path4 = os.path.join(path, "hotmaps_task_2.7_load_profile_tertiary_shw_yearlong_2010_part2.csv")
    paths = [path1, path2]
    # determine delimiter of csv file
    data = pd.DataFrame(columns=("NUTS2_code", "process", "hour", "load"))
    for path in paths:
        with open(path, 'r', encoding='utf-8') as csv_file:
            delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
        dat = pd.read_csv(path, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
        data = data.append(dat)
    data = data[data["NUTS2_code"].isin(nuts2_ids)]

    paths = [path3, path4]
    data2 = pd.DataFrame(columns=("NUTS2_code", "process", "hour", "load"))
    for path in paths:
        with open(path, 'r', encoding='utf-8') as csv_file:
            delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
        dat = pd.read_csv(path, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
        data2 = data2.append(dat)
    data2 = data2[data2["NUTS2_code"].isin(nuts2_ids)]

    return data, data2


def ad_industrial_database_local(nuts2_ids):
    """
    loads data of heat sources given by a csv file.

    :return: dataframe containing the data of the csv file.
    :rtype: pandas dataframe.
    """

    country_to_nuts0 = {"Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Cyprus": "CY", "Czech Republic": "CZ",
                        "Germany": "DE", "Denmark": "DK", "Estonia": "EE", "Finland": "FI", "France": "FR",
                        "Greece": "EL", "Hungary": "HU", "Croatia": "HR", "Ireland": "IE", "Italy": "IT",
                        "Lithuania": "LT", "Luxembourg": "LU", "Latvia": "LV", "Malta": "MT", "Netherland": "NL",
                        "Netherlands": "Nl",
                        "Poland": "PL", "Portugal": "PT", "Romania": "RO", "Spain": "ES", "Sweden": "SE",
                        "Slovenia": "SI", "Slovakia": "SK", "United Kingdom": "UK", "Albania": "AL", "Montenegro": "ME",
                        "North Macedonia": "MK", "Serbia": "RS", "Turkey": "TR", "Switzerland": "CH", "Iceland": "IS",
                        "Liechtenstein": "LI", "Norway": "NO"}
    path = os.path.dirname(
           os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(os.path.join(path, "data"), "Industrial_Database.csv")

    # determine delimiter of csv file
    with open(path, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter

    raw_data = pd.read_csv(path, sep=delimiter, usecols=("geom", "Subsector", "Excess_Heat_100-200C",
                                                         "Excess_Heat_200-500C", "Excess_Heat_500C", "Country", "Nuts2_ID"))
    raw_data = raw_data[raw_data["Nuts2_ID"].isin(nuts2_ids)]
    # dataframe for processed data
    data = pd.DataFrame(columns=("ellipsoid", "Lon", "Lat", "Nuts0_ID", "Subsector", "Excess_heat", "Temperature", "Nuts2_ID"))

    for i, site in raw_data.iterrows():
        # check if site location is available
        if not pd.isna(site["geom"]):
            # extract ellipsoid model and (lon, lat) from the "geom" column
            ellipsoid, coordinate = site["geom"].split(";")
            m = re.search("[-+]?[0-9]*\.?[0-9]+.[-+]?[0-9]*\.?[0-9]+", coordinate)
            m = m.group(0)
            lon, lat = m.split(" ")
            lon = float(lon)
            lat = float(lat)

            nuts0 = country_to_nuts0[site["Country"]]

            # check if heat at specific temperature range is available
            # TODO deal with units; hard coded temp ranges?
            if not pd.isna(site["Excess_Heat_100-200C"]) and site["Excess_Heat_100-200C"] != "" and site["Excess_Heat_100-200C"] != 0:
                data.loc[data.shape[0]] = (ellipsoid, lon, lat, nuts0, site["Subsector"],
                                           site["Excess_Heat_100-200C"] * 1000, 150, site["Nuts2_ID"])
            if not pd.isna(site["Excess_Heat_200-500C"]) and site["Excess_Heat_200-500C"] != "" and site["Excess_Heat_200-500C"] != 0:
                data.loc[data.shape[0]] = (ellipsoid, lon, lat, nuts0,
                                           site["Subsector"], site["Excess_Heat_200-500C"] * 1000, 350, site["Nuts2_ID"])
            if not pd.isna(site["Excess_Heat_500C"]) and site["Excess_Heat_500C"] != "" and site["Excess_Heat_500C"] != 0:
                data.loc[data.shape[0]] = (ellipsoid, lon, lat, nuts0,
                                           site["Subsector"], site["Excess_Heat_500C"] * 1000, 500, site["Nuts2_ID"])

    return data


def raster_array(raster, dType=float, return_gt=None):
    ds = gdal.Open(raster)
    geo_transform = ds.GetGeoTransform()
    band1 = ds.GetRasterBand(1)
    arr = band1.ReadAsArray().astype(dType)
    ds = None
    if return_gt:
        return arr, geo_transform
    else:
        return arr


def ad_nuts_id():
    path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "data")
    path = os.path.join(path, "data_nuts_id_number.csv")
    with open(path, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter

    data = pd.read_csv(path, sep=delimiter)
    return data
