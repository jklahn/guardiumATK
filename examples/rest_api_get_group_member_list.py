from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'group_members_by_group_desc' REST API is used 
to list the members of a group, using the group name as the identifier.

Group API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-group-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: List group members based on group name
result = guardium_api.get_group_members_by_desc(params={
    'desc': 'Sensitive Objects',  # [str] [required]; -- name of the group to get the list of members
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Examples:
    # 'all_managed': execute on all managed units but not the central manager
    # 'all': execute on all managed units and the central manager
})

print(result)
