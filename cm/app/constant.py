
CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'



CM_REGISTER_Q = 'rpc_queue_CM_register'
CM_NAME = 'Load profile CM'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE'
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 7
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80
#TODO***********************************************************************
CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER
#TODO***********************************************************************

TRANFER_PROTOCOLE ='http://'

INPUTS_CALCULATION_MODULE = [

    {'input_name': 'Residential heating',
     'input_type': 'range',
     'input_parameter_name': 'res_heating_share',
     'input_value': 0.33,
     'input_unit': '',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },
    {'input_name': 'Industry',
     'input_type': 'range',
     'input_parameter_name': 'industry_share',
     'input_value': 0.33,
     'input_unit': '',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },
    {'input_name': 'Tertiary heating',
     'input_type': 'range',
     'input_parameter_name': 'tertiary_share',
     'input_value': 0.33,
     'input_unit': '',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },

]


SIGNATURE = {
    "category": "Buildings",
    "cm_name": CM_NAME,
    "layers_needed": [
    ],
    "vectors_needed": [
    ],
    "type_layer_needed": [
    ],
    "cm_url": "Do not add something",
    "cm_description": "CM generating new load profiles",
    "cm_id": CM_ID,
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
