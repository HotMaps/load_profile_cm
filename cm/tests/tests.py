import unittest
from werkzeug.exceptions import NotFound
from app import create_app
import os.path
from shutil import copyfile
from .test_client import TestClient

import json as json_lib
#CM provider are not alloed to change the upload directory
UPLOAD_DIRECTORY = 'home/david/var/hotmaps/cm_files_uploaded'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    os.chmod(UPLOAD_DIRECTORY, 0o777)


class TestAPI(unittest.TestCase):


    def setUp(self):
        self.app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = TestClient(self.app,)

    def tearDown(self):

        self.ctx.pop()


    def test_compute(self):
        # simulate copy from HTAPI to CM

        heat_total = "tests/data/pl22_total.tif"
        heat_total_save_path = UPLOAD_DIRECTORY + "/heat_total.tif"
        copyfile(heat_total, heat_total_save_path)

        heat_res = "tests/data/pl22_res.tif"
        heat_res_save_path = UPLOAD_DIRECTORY + "/heat_res.tif"
        copyfile(heat_res, heat_res_save_path)

        heat_nonres = "tests/data/pl22_nonres.tif"
        heat_nonres_save_path = UPLOAD_DIRECTORY + "/heat_nonres.tif"
        copyfile(heat_nonres, heat_nonres_save_path)

        nuts_id = "tests/data/pl22_nuts.tif"
        nuts_id_save_path = UPLOAD_DIRECTORY + "/nuts.tif"
        copyfile(nuts_id, nuts_id_save_path)

        gfa_res_curr = "tests/data/gfa_res_curr_density_pl22.tif"
        gfa_res_curr_save_path = UPLOAD_DIRECTORY + "/gfa_res.tif"
        copyfile(gfa_res_curr, gfa_res_curr_save_path)

        gfa_nonres_curr = "tests/data/gfa_nonres_curr_density_pl22.tif"
        gfa_nonres_curr_save_path = UPLOAD_DIRECTORY + "/gfa_nonres.tif"
        copyfile(gfa_nonres_curr, gfa_nonres_curr_save_path)

        inputs_raster_selection = {}
        inputs_parameter_selection = {}
        inputs_vector_selection = {}

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_industry_chemicals_and_petrochemicals_yearlong_2018_dk.json', 'r') as file:
        #    inputs_vector_selection["load_profile_industry_chemicals_and_petrochemicals_yearlong_2018"] = json_lib.load(file)

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_industry_food_and_tobacco_yearlong_2018_dk.json', 'r') as file:
        #    inputs_vector_selection["load_profile_industry_food_and_tobacco_yearlong_2018"] = json_lib.load(file)

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_industry_iron_and_steel_yearlong_2018_dk.json', 'r') as file:
        #    inputs_vector_selection["load_profile_industry_iron_and_steel_yearlong_2018"] = json_lib.load(file)

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_industry_non_metalic_minerals_yearlong_2018_dk.json', 'r') as file:
        #    inputs_vector_selection["load_profile_industry_non_metalic_minerals_yearlong_2018"] = json_lib.load(file)

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_industry_paper_yearlong_2018_dk.json', 'r') as file:
        #    inputs_vector_selection["load_profile_industry_paper_yearlong_2018"] = json_lib.load(file)

        #with open('tests/data/data_hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010_dk05.json', 'r') as file:
        #    inputs_vector_selection["load_profile_residential_heating_yearlong_2010"] = json_lib.load(file)

        #with open('tests/data/industrial_Database_dk.json', 'r') as file:
        #    inputs_vector_selection["industrial_database"] = json_lib.load(file)

        inputs_parameter_selection["res_heating_share"] = 0.33
        inputs_parameter_selection["industry_share"] = 0.33
        inputs_parameter_selection["tertiary_share"] = 0.33
        nuts = ['PL22']

        inputs_raster_selection["heat_tot_curr_density"] = heat_total_save_path
        inputs_raster_selection["heat_res_curr_density"] = heat_res_save_path
        inputs_raster_selection["heat_nonres_curr_density"] = heat_nonres_save_path
        inputs_raster_selection["gfa_res_curr_density"] = gfa_res_curr_save_path
        inputs_raster_selection["gfa_nonres_curr_density"] = gfa_nonres_curr_save_path
        inputs_raster_selection["nuts_id_number"] = nuts_id_save_path

        # register the calculation module a
        payload = {"inputs_raster_selection": inputs_raster_selection,
                   "inputs_parameter_selection": inputs_parameter_selection,
                   "inputs_vector_selection": inputs_vector_selection,
                   "nuts": nuts}


        rv, json = self.client.post('computation-module/compute/', data=payload)
        has_indicators = False

        cm_name = json['result']['name']
        print ('cm_name ', type(cm_name))
        try:
            indicators = json['result']['indicator']
            has_indicators = True

        except:
            pass
        #test is the value are string
        if has_indicators == True:
            for ind in indicators:
                value = ind['value']
                print ('value ', type(value))
                self.assertIs(type(value), str)
        if has_indicators == True:
            for ind in indicators:
                value = ind['value']
                print ('value ', type(value))
                self.assertTrue(value != -888888888)







        self.assertTrue(rv.status_code == 200)


