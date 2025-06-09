from guardiumATK import rest_api_functions
import pandas

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, GET 'ruleInfoFromPolicy' REST API is called to get 
a detailed list of rules for a given policy - which includes actions and continuance criteria.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-list-policy-rules
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""

guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

result = guardium_api.get_list_of_policy_rules_detailed(params={
    'policyDesc': 'Basic Data Security Policy',  # [str][required]; Name of the policy
    'api_target_host': '',  # [str]; host name or IP address of the central manager
    'localeLanguage': 0  # [int]; 0 (false), 1 (true)
    })

# print list of JSONs dictionaries for each rule
print("\nPolicy rules as a list of dictionaries:")
print(result)


# converts the list of dictionaries into a pretty table
print("\nPolicy is truncated table format:")
pd = pandas
pd.options.display.width = 0
print(pandas.DataFrame(result))
