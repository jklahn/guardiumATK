from guardiumATK import rest_api_functions

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'policy_install', 'reinstall_policy', and 
'policy_uninstall' REST APIs is used to uninstall or install an existing policy.

References: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-policy-install
https://www.ibm.com/docs/en/gdp/12.x?topic=reference-policy-uninstall
https://www.ibm.com/docs/en/gdp/12.x?topic=reference-reinstall-policy
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis

"""

guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Install a policy
result = guardium_api.post_install_policy(params={
    'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy or policies to install.
                                # Use a pipe ( | ) character to separate multiple policies.
    'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
            })

print(result)

# Example: Uninstall a policy
# result = guardium_api.post_uninstall_policy(params={
#     'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy to uninstall.
#     'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
#             })

# print(result)

# Example: Re-install a policy
# result = guardium_api.post_reinstall_policy(params={
#     'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy to re-install.
#     'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes. Example: all_managed
#             })
#
# print(result)
