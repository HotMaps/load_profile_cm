import pandas as pd
import os
import csv





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

    # determine delimiter of csv file
    with open(path1, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
    data = pd.read_csv(path1, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
    with open(path2, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
    data2 = pd.read_csv(path2, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))

    data = data.append(data2)
    data = data[data["NUTS2_code"].isin(nuts2_ids)]

    return data


def ad_tertiary_profile_local(nuts2_ids):
    """
    Loads residential heating profiles from csv file.

    :return: Dataframe containing the data of the csv file.
    :rtype: pandas dataframe.
    """

    path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "data")
    path1 = os.path.join(path, "hotmaps_task_2.7_load_profile_tertiary_shw_yearlong_2010_part1.csv")
    path2 = os.path.join(path, "hotmaps_task_2.7_load_profile_tertiary_shw_yearlong_2010_part2.csv")

    # determine delimiter of csv file
    with open(path1, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
    data = pd.read_csv(path1, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))
    with open(path2, 'r', encoding='utf-8') as csv_file:
        delimiter = csv.Sniffer().sniff(csv_file.readline()).delimiter
    data2 = pd.read_csv(path2, sep=delimiter, usecols=("NUTS2_code", "process", "hour", "load"))

    data = data.append(data2)
    data = data[data["NUTS2_code"].isin(nuts2_ids)]

    return data

