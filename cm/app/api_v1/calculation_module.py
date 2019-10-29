from osgeo import gdal
from ..constant import CM_NAME

from ..helper import generate_output_file_tif, create_zip_shapefiles, generate_output_file_shp, generate_output_file_csv
import time
""" Entry point of the calculation module function"""

from .my_calculation_module_directory import run_cm

""" Entry point of the calculation module function"""

# TODO: CM provider must "change this code"
# TODO: CM provider must "not change input_raster_selection,output_raster  1 raster input => 1 raster output"
# TODO: CM provider can "add all the parameters he needs to run his CM
# TODO: CM provider can "return as many indicators as he wants"


def calculation(output_directory, inputs_raster_selection, inputs_vector_selection, inputs_parameter_selection, nuts):
    """ def calculation()"""

    heat_density_raster_res = inputs_raster_selection["heat_res_curr_density"]
    heat_density_raster_nonres = inputs_raster_selection["heat_nonres_curr_density"]
    gfa_res_curr_density = inputs_raster_selection["gfa_res_curr_density"]
    gfa_nonres_curr_density = inputs_raster_selection["gfa_nonres_curr_density"]
    nuts_id_number = inputs_raster_selection["nuts_id_number"]

    res_heating_factor = float(inputs_parameter_selection["res_heating_factor"])
    ter_heating_factor = float(inputs_parameter_selection["ter_heating_factor"])
    res_water_factor = float(inputs_parameter_selection["res_water_factor"])
    ter_water_factor = float(inputs_parameter_selection["ter_water_factor"])

    # lp_chemical = inputs_vector_selection["load_profile_industry_chemicals_and_petrochemicals_yearlong_2018"]
    # lp_food = inputs_vector_selection["load_profile_industry_food_and_tobacco_yearlong_2018"]
    # lp_iron = inputs_vector_selection["load_profile_industry_iron_and_steel_yearlong_2018"]
    # lp_non_metalic = inputs_vector_selection["load_profile_industry_non_metalic_minerals_yearlong_2018"]
    # lp_paper = inputs_vector_selection["load_profile_industry_paper_yearlong_2018"]
    # industry_profiles = [lp_chemical, lp_food, lp_iron, lp_non_metalic, lp_paper]

    # sink_profiles = inputs_vector_selection["load_profile_residential_heating_yearlong_2010"]

    output_csv_path_1 = generate_output_file_csv(output_directory)

    results = run_cm.main(res_heating_factor, ter_heating_factor, res_water_factor, ter_water_factor, heat_density_raster_res, heat_density_raster_nonres, gfa_res_curr_density, gfa_nonres_curr_density, nuts_id_number, output_csv_path_1)

    if results[0] == -1:
        result = dict()
        result['name'] = CM_NAME
        result['indicator'] = [{"unit": " ", "name": results[1],
                                "value": "0"}]
        return result

    graphics, total_industry, total_res_heating, total_res_shw, total_ter_heating, total_ter_shw, total_heat = results


    def round_to_n(x, n):
        length = 0
        if x > 1:
            while x > 1:
                x /= 10
                length += 1
        elif x == 0:
            return 0
        else:
            while x < 1:
                x *= 10
                length -= 1

        return round(x, n) * 10 ** length

    result = dict()

    result["graphics"] = graphics

    result['indicator'] = [{"unit": "GWh", "name": "Heat demand in GWh by industry",
                        "value": str(round_to_n(total_industry, 3))},
                       {"unit": "GWh", "name": "Heat demand in GWh by residential heating",
                        "value": str(round_to_n(total_res_heating, 3))},
                           {"unit": "GWh", "name": "Heat demand in GWh by residential warm water supply",
                        "value": str(round_to_n(total_res_shw,3))},
                           {"unit": "GWh", "name": "Heat demand in GWh by tertiary sector heating",
                        "value": str(round_to_n(total_ter_heating,3))},
                           {"unit": "GWh", "name": "Heat demand in GWh by tertiary sector warm water supply",
                        "value": str(round_to_n(total_ter_shw,3))},
                              {"unit": "GWh", "name": "Total heat demand in GWh",
                        "value": str(round_to_n(total_heat,3))}]

    result["csv_files"] = [{"Load profile": "csv 1", "path": output_csv_path_1}]

    result['name'] = CM_NAME

    return result


def colorizeMyOutputRaster(out_ds):
    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0,0,0,255))
    ct.SetColorEntry(1, (110,220,110,255))
    out_ds.SetColorTable(ct)
    return out_ds
