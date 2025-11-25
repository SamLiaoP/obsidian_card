接需求：

  

{

"order_data": {

"ip": "11.22.33.44",

"phone_number": "36200130525",

"email": "daguanting@gmail.com"

},

"mission_name": "seon_test",

"mission_report_path": "report_customer"

  

}

  

  

傳遞後續任務：

  

{

"mission_name": "seon_test",

"mission_id": "mission_test_1206",

"task_report_path": "repot_liaison"

"task_name": "call_seon_fraud_api",

"task_id": "call_call_call_what",

"task_sequence":"1"

"task_status":"Success"

  

}

  

  

  

config:

  

{

"seon_test": {

"common_message": {

"mission_name": "seon_test",

"mission_id": "",

"task_report_path": "repot_liaison"

},

"1": {

"order_data": {

"ip": "",

"phone_number": "",

"email": ""

},

  

"executor": "scout",

"previous_task_id": "",

"task_name": "call_seon_fraud_api",

"task_id": "",

"task_sequence": 1,

"raw_table_path": "SAM_LAB.MISSION_NAME_RAW_TABLE_test_1129",

"task_status": "start"

},

"2": {

"order_data": {

"select_conditions": [

  

"TASK_ID = '{previous_task_id}'"

]

},

"task_name": "customize_select",

"task_id": "cus_select_test",

"previous_task_id": "",

"task_sequence": 2,

"source_table_path": "SAM_LAB.MISSION_NAME_RAW_TABLE_test_1129",

"destination_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1206",

"task_status": "start",

"use_general_tmp_table": true

},

"3": {

"order_data": {

"columns": "RAW_DATA"

},

"task_name": "flatten_json",

"task_id": "flat_json_test",

"previous_task_id": "cus_select_test",

"task_sequence": 3,

"source_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1206",

"destination_table_path": "SAM_LAB.SEON_TEST_1208",

"task_status": "start",

"use_general_tmp_table": false

}

}

  

}