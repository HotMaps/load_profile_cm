CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'



CM_REGISTER_Q = 'rpc_queue_CM_register'
CM_NAME = 'CM - Heat load profiles'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE'
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 9
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80
#TODO***********************************************************************
CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER
#TODO***********************************************************************

TRANFER_PROTOCOLE ='http://'

INPUTS_CALCULATION_MODULE = [

    {'input_name': 'Residential heating factor',
     'input_type': 'input',
     'input_parameter_name': 'res_heating_factor',
     'input_value': 1,
     'input_unit': ' ',
     'input_min': 0,
     'input_max': 10,
     'cm_id': CM_ID
     },
    {'input_name': 'Tertiary heating factor',
     'input_type': 'input',
     'input_parameter_name': 'ter_heating_factor',
     'input_value': 1,
     'input_unit': ' ',
     'input_min': 0,
     'input_max': 10,
     'cm_id': CM_ID
     },
    {
    'input_name': 'Residential hot water supply factor',
     'input_type': 'input',
     'input_parameter_name': 'res_water_factor',
     'input_value': 1,
     'input_unit': ' ',
     'input_min': 0,
     'input_max': 10,
     'cm_id': CM_ID
     },
    {'input_name': 'Tertiary hot water supply factor',
     'input_type': 'input',
     'input_parameter_name': 'ter_water_factor',
     'input_value': 1,
     'input_unit': ' ',
     'input_min': 0,
     'input_max': 10,
     'cm_id': CM_ID
     }


]

SIGNATURE = {
    "category": "Demand",
    "cm_name": CM_NAME,
    "layers_needed": [
        "heat_res_curr_density",
        "heat_nonres_curr_density",
        "nuts_id_number",
        "gfa_res_curr_density",
        "gfa_nonres_curr_density"
    ],
    "vectors_needed": [
        # "lp_residential_shw_and_heating_yearlong_2010",
        # "lp_industry_iron_and_steel_yearlong_2018",
        # "lp_industry_paper_yearlong_2018",
        # "lp_industry_non_metalic_minerals_yearlong_2018",
        # "lp_industry_food_and_tobacco_yearlong_2018",
        # "lp_industry_chemicals_and_petrochemicals_yearlong_2018"
    ],
    "type_layer_needed": [
        {"type": "heat_res_curr_density", "description": "Select heat demand residential density layer."},
        {"type": "heat_nonres_curr_density", "description": "Select heat demand teritary density layer."},
        {"type": "nuts_id_number"},
        {"type": "gfa_res_curr_density", "description": "Select gross floor area residential layer"},
        {"type": "gfa_nonres_curr_density", "description": "Select gross floor area tertiary layer"}
    ],

    "cm_url": "Do not add something",
    "cm_description": "This caluclation module can be used to generate new load profiles based on the Hotmaps default load profile data set.",
    "cm_id": CM_ID,
    "wiki_url":"https://wiki.hotmaps.eu/en/CM-Heat-load-profiles",
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}



