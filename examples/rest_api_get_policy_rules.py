from guardiumATK.rest_api_functions import GuardiumRESTAPI
import pandas

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, GET 'rule' REST API is called to get a list of
rules for a given policy.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-list-policy-rules
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""

guardium_api = GuardiumRESTAPI()

# returns a list of policy rules - each rule is a dictionary
result = guardium_api.get_list_of_policy_rules(params={
    'policy': 'Basic Data Security Policy',  # [str][required]; Name of the policy
    'api_target_host': ''  # [str]; Specifies the target hosts where the API executes
})

# converts the list of dictionaries into a pretty table
pd = pandas
pd.options.display.width = 0
print(pandas.DataFrame(result))
