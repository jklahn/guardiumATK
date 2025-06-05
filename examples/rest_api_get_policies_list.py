from guardiumATK.rest_api_functions import GuardiumRESTAPI
import pandas

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, GET 'policy' REST API is called to get a list of
Guardium policies (both active and inactive).

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-list-policy
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""

guardium_api = GuardiumRESTAPI()

# returns a list of policies or policy details
result = guardium_api.get_list_of_policies(params={
    'detail': 1,  # int; Display details about a policy (or all policies if you do not specify a
    # policyDesc). Valid values: 0(false),1 (true)
    'policyDesc': '',  # [str] -- The name of one policy to display. If not specified, Guardium returns
    # information about all available policies.
    'verbose': 0,  # [int] -- 0(false),1 (true)
    'api_target_host': ''  # str; Specifies the target hosts where the API executes
})

# converts the list of dictionaries into a pretty table
pd = pandas
pd.options.display.width = 0
print(pandas.DataFrame(result))
