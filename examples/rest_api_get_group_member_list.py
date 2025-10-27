from guardiumATK import rest_api_functions
import pandas

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'group_members_by_group_desc' REST API is used 
to list the members of a group, using the group name as the identifier.

Group API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-group-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: List group members based on group name ('description')
result = guardium_api.get_group_members_by_desc(params={
    'desc': 'Sensitive Objects',  # [str] [required]; -- name of the group to get the list of members
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Examples:
    # 'all_managed': execute on all managed units but not the central manager
    # 'all': execute on all managed units and the central manager
})

'''Example result:
{'group_id': 5, 'group_description': 'Sensitive Objects', 'group_members': [{'member': '%/%.CUSTOMER'},... '''

# extracting just the 'group_members' piece of the json result
group_members_list_raw = result['group_members']

'''Example group_members_list_raw
[{'member': '%/%.CUSTOMER'}, {'member': '%/%.CUSTOMER_ADDRESS'}, {'member': '%/%.CUSTOMER_DEMOGRAPHICS'}...'''

# raw list is a list of dictionaries - needs cleaned up to just be a list of strings
group_members_list_cleaned = []
for member in group_members_list_raw:
    group_members_list_cleaned.append(member['member'])

print(group_members_list_cleaned)  # cleaned up result - a list of strings for the group
