from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'rule' REST API is used to add a rule
to an existing policy.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-create-rule
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Add action to existing policy rule
result = guardium_api.post_add_rule_to_policy(params={
    'fromPolicy': '-ChuckWasHere',  # [str] [required]; -- Policy name to add the rule to
    'ruleType': 'ACCESS',  # [str] [required]; -- Valid values: ACCESS, EXCEPTION, EXTRUSION, MASK_ON_SCREEN,
    # MASK_ON_DB, MASK_ON_MONGODB, DATASET_COLLECTION_PROFILE, DB2_COLLECTION_PROFILE, DB2_BLOCKING_PROFILE,
    # IMS_COLLECTION_PROFILE, SESSION
    'category': '',  # [str]; -- Access, Activity, Audit, Audit Mode, BASEL II, CCPA, Data Privacy...
    'classification': '',  # [str];
    'order': '',  # [int];
    'ruleDesc': 'Log DML',  # [str] [required]; -- Unique name for the rule
    'ruleLevel': '',  # [str];
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
            })

print(result)
