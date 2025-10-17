from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'group' REST API is used to create a group.

Group API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-group-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Create group
result = guardium_api.post_create_group(params={
    'appid': 'Public',  # [str] [required]; -- Example: Public, Classifier, Policy Builder
    'category': '',  # [str]; -- optional label that is used to group policy violations and groups for reporting
    'classification': '',  # [str]; -- optional label that is used to group policy violations and groups for reporting
    'desc': 'My Custom Tuple Group',  # [str] [required]; -- a unique description for the new group
    'hierarchical': '',  # [str]; -- 'true' / 'false' (default); indicates if the group is meant to contain other groups
    # (hierarchical)
    'tuple_parameters': 'client_ip,client_host_name,server_ip',  # [str]; -- if group type is 'Tuples', then use a
    # comma separated list (no space between values) of at least one tuple parameter to define the tuple.
    # Valid parameters: client_ip, client_host_name, server_ip, server_host_name, source_program, db_name, db_user,
    # service_name, app_user_name, os_user, db_type, net_protocol, command, server_port, sender_ip, server_description,
    # analyzed_client_ip, incident, session, client_os_name, server_os_name, db_prototype, field_name, error_code
    'type': 'Tuples'  # [str] [required]; -- type of group. Examples: COMMANDS, Database Name, OBJECTS, USERS, Tuples
})

print(result)
