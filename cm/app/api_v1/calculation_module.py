from osgeo import gdal

from ..helper import generate_output_file_tif, create_zip_shapefiles, generate_output_file_shp, generate_output_file_csv
import time
""" Entry point of the calculation module function"""

from .my_calculation_module_directory import run_cm

""" Entry point of the calculation module function"""

# TODO: CM provider must "change this code"
# TODO: CM provider must "not change input_raster_selection,output_raster  1 raster input => 1 raster output"
# TODO: CM provider can "add all the parameters he needs to run his CM
# TODO: CM provider can "return as many indicators as he wants"


def calculation(output_directory, inputs_raster_selection, input_vector_selection, inputs_parameter_selection, nuts):
    """ def calculation()"""
    '''
    inputs:
        hdm in raster format for the selected region
        pix_threshold [GWh/km2]
        DH_threshold [GWh/a]

    Outputs:
        DH_Regions: contains binary values (no units) showing coherent areas
    '''
    res_heating_share = inputs_parameter_selection["res_heating_share"]
    industry_share = inputs_parameter_selection["industry_share"]
    tertiary_share = inputs_parameter_selection["tertiary_share"]

    nuts2_id = nuts
    print('type nuts', type(nuts2_id))

    # industrial_sites = inputs_vector_selection["industrial_database"]

    # lp_chemical = inputs_vector_selection["load_profile_industry_chemicals_and_petrochemicals_yearlong_2018"]
    # lp_food = inputs_vector_selection["load_profile_industry_food_and_tobacco_yearlong_2018"]
    # lp_iron = inputs_vector_selection["load_profile_industry_iron_and_steel_yearlong_2018"]
    # lp_non_metalic = inputs_vector_selection["load_profile_industry_non_metalic_minerals_yearlong_2018"]
    # lp_paper = inputs_vector_selection["load_profile_industry_paper_yearlong_2018"]
    # industry_profiles = [lp_chemical, lp_food, lp_iron, lp_non_metalic, lp_paper]

    # sink_profiles = inputs_vector_selection["load_profile_residential_heating_yearlong_2010"]

    output_csv_path_1 = generate_output_file_csv(output_directory)

    graphics = run_cm.main(res_heating_share, industry_share, tertiary_share, nuts2_id, output_csv_path_1)
    
    result = dict()

    result["graphics"] = graphics
    
    result["csv_files"] = [{"Load profile": "csv 1", "path": output_csv_path_1}]

    result['name'] = 'CM - Heat load profiles'


    return result


def colorizeMyOutputRaster(out_ds):
    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0,0,0,255))
    ct.SetColorEntry(1, (110,220,110,255))
    out_ds.SetColorTable(ct)
    return out_ds
