from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'policy' REST API is used to create a
new policy.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-create-policy
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Create policy
result = guardium_api.post_create_policy(params={
    'ruleSetDesc': '-ChuckWasHere',  # [str][required]; -- The name of the policy to be created.
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
