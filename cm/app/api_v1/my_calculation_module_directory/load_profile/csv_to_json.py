import json
import csv

csv.register_dialect('myDialect',
delimiter = ',',
skipinitialspace=True)

def csv_to_json(csv_file, json_file):
    jsonfile = open(json_file, "w")
    with open(csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, dialect="myDialect")
        header = next(reader)
        print(header)
        reader = csv.DictReader(file, fieldnames=header, dialect="myDialect")
        json.dump([row for row in reader], jsonfile, indent=2)

#csv_to_json("C:\\Users\\david\\Documents\\Documents\\Fraunhofer\\Hotmaps\\data\\test_data2\\data_hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010_dk05.csv",
#            "C:\\Users\\david\\Documents\\Documents\\Fraunhofer\\Hotmaps\\CM_excess_heat\cm\\tests\\data\\data_hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010_dk05.json")
with open("C:\\Users\\david\\Documents\\Documents\\Fraunhofer\\Hotmaps\\CM_excess_heat\cm\\tests\\data\\data_hotmaps_task_2.7_load_profile_industry_chemicals_and_petrochemicals_yearlong_2018_dk.json", "r") as file:
    data = json.load(file)

print(data)