
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

    {'input_name': 'Residential heating',
     'input_type': 'input',
     'input_parameter_name': 'res_heating_share',
     'input_value': 0.33,
     'input_unit': 'none',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },
    {'input_name': 'Industry',
     'input_type': 'input',
     'input_parameter_name': 'industry_share',
     'input_value': 0.33,
     'input_unit': 'none',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },
    {'input_name': 'Tertiary heating',
     'input_type': 'input',
     'input_parameter_name': 'tertiary_share',
     'input_value': 0.33,
     'input_unit': 'none',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     }

]
INPUTS_CALCULATION_MODULE2 = [

    {'input_name': 'Min. heat demand in hectare',
     'input_type': 'input',
     'input_parameter_name': 'pix_threshold',
     'input_value': 333,
     'input_unit': 'MWh/ha',
     'input_min': 0,
     'input_max': 1000,
     'cm_id': CM_ID
     },
    {'input_name': 'Min. heat demand in a DH area',
     'input_type': 'input',
     'input_parameter_name': 'DH_threshold',
     'input_value': 30,
     'input_unit': 'GWh/year',
     'input_min': 0,
     'input_max': 500,
     'cm_id': CM_ID
     }
]

SIGNATURE2 = {
    "category": "Buildings",
    "cm_name": CM_NAME,
    "layers_needed": [
        "heat_tot_curr_density_tif",
    ],
    "type_layer_needed": [
        "heat",
    ],
    "cm_url": "Do not add something",
    "cm_description": "CM generating new load profiles",
    "cm_id": CM_ID,
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
SIGNATURE = {
    "category": "Buildings",
    "cm_name": CM_NAME,
    "layers_needed": [
        "heat_tot_curr_density_tif",
    ],
    "type_layer_needed": [
        "heat",
    ],
    "cm_url": "Do not add something",
    "cm_description": "This computation module calculates district heating " \
                      "potential within the selected region. As output, a layer for the " \
                      "potential areas are shown. Click on the regions to get their " \
                      "corresponding potential. Within the indicator/graph window, relevant " \
                      "indicators and charts regarding DH potential within the selected zone" \
                      "and potentials in sub-zones are illustrated.",
    "cm_id": CM_ID,
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
