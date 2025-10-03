from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'policy' REST API is used to delete an existing 
policy.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-delete-policy
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Delete policy
result = guardium_api.delete_policy(params={
    'policyDesc': '-ChuckWasHere',  # [str][required]; -- The name of the policy to be deleted.
    'api_target_host': '',  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
            })

print(result)
