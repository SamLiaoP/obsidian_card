sapper 會需要一張 temp 表

  

做客製化select

{

  "order_data": {

    "select_conditions": ["JOB_ID = '{previous_job_id}'"]

  },

  "mission_name": "seon_test",

  "mission_id": "mission_test_1206",

  "job_name": "customize_select",

  "job_id": "cus_select_test",

  "previous_job_id": "755ab57c-b55f-45cf-8a32-073001e0c463",

  "job_sequence": 2,

  "job_report_path": "repot_liaison",

  "source_table_path": "SAM_LAB.RAW_SEON_test_1215",

  "destination_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1215",

  "job_status": "start",

  "use_general_tmp_table": true

}

  

做json攤平

{

  "order_data": {

    "columns": "RAW_DATA"

  },

  "mission_name": "seon_test",

  "mission_id": "mission_test_1206",

  "job_name": "flatten_json",

  "job_id": "flat_json_test",

  "previous_job_id":"cus_select_test",

  "job_sequence": 3,

  "report_path": "repot_liaison",

  "source_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1206",

  "destination_table_path" : "SAM_LAB.SEON_TEST_1208",

  "job_status": "start",

"use_general_tmp_table": false

}