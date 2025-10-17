from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'group' REST API is used to delete a group.

Group API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-group-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Create group
result = guardium_api.delete_group_by_desc(params={
    'desc': 'My Custom Tuple Group',  # [str] [required]; -- name of the group to be deleted
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Examples:
    # 'all_managed': execute on all managed units but not the central manager
    # 'all': execute on all managed units and the central manager
})

print(result)
