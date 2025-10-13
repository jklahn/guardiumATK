from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, we use multiple policy APIs to create a policy,
policy rule, and add an action to the policy rule.

Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Create policy
result = guardium_api.post_create_policy(params={
    'ruleSetDesc': '-TechXchange2025',  # [str][required]; -- The name of the policy to be created.
    'baselineDesc': '',  # [str];
    'categoryName': '',  # [str]; -- Category of the policy, Example: 'Access', 'Activity', 'SOX'
    'isFam': '',  # [boolean]; -- Determines whether this policy is for file access monitoring. Valid values:
                    # 0 (false): This is a data access monitoring policy.
                    # 1 (true): This is a file access monitoring policy.
    'logFlat': '',  # [boolean]; -- Determine whether to use the flat log option for this policy. Valid values:
                    # 0 (false)
                    # 1 (true)
    'pattern': '',  # [str]; -- A regular expression to match. Log based on a regular expression to match on the SQL.
    'policyLevel': '',  # [str]; -- Valid values: REGULAR [DEFAULT], SESSION, FAM, FAM_SP, FAM_NAS, 0, 1, 2, 3, 4
    'rulesOnFlat': '',  # [boolean]; -- Valid values: 0 (false)[DEFAULT], 1 (true)
    'securityPolicy': 'true',  # [boolean]; -- Selective audit disabled (false, default), enabled (true)
    'api_target_host': '',  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
            })

print(result)

# Example: Add rule to policy
result = guardium_api.post_add_rule_to_policy(params={
    'fromPolicy': '-TechXchange2025',  # [str] [required]; -- Policy name to add the rule to
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

# Example: Add action to policy rule
result = guardium_api.post_policy_rule_action(params={
    'fromPolicy': '-TechXchange2025',  # str; required -- policy name
    'ruleDesc': 'Log DML',  # str; required -- rule name, Example: 'SQL Error - Log'
    'actionName': 'LOG MASKED DETAILS',  # str; required - Example: 'LOG FULL DETAILS PER SESSION'
    'actionLevel': '',  # str;
    'actionParameters': '',  # str;
    'alertUserLoginName': '',  # str;
    'classDestination': '',  # str;
    'messageTemplate': '',  # str; -- Examples: Default, LEEF
    'notificationType': '',  # str; -- Examples: MAIL, SYSLOG, SNMP
    'paramSeparator': ''  # str;
            })

print(result)

# Example: Install policy
result = guardium_api.post_install_policy(params={
    'policy': '-TechXchange2025|Basic Data Security Policy',  # [str] [required]; -- The name of the policy or
    # policies to install. Use a pipe ( | ) character to separate multiple policies.
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
            })

print(result)
