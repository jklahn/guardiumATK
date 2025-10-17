from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'group_member' REST API is used to add a
member to an existing group.

Group API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-group-apis
"""


guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: add member to group using the group name
result = guardium_api.post_add_member_to_group_by_desc(params={
    'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to add the member to
    'member': '%CREDIT'  # [str] [required]; -- The member name (must be unique within the group)
            })

print(result)

# Another example, this time using a list of members to add to a group
new_members_to_add = ['%JOSH', '%CARD', '%DOD', 'IBM']

for member in new_members_to_add:
    result = guardium_api.post_add_member_to_group_by_desc(params={
        'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to add the member to
        'member': member  # [str] [required]; -- The member name (must be unique within the group)
    })

    print(result)

