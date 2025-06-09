# guardiumATK
`guardiumATK` (Guardium Automation ToolKit) provides a pythonic package to automate tasks in Guardium. Leveraging
both REST APIs and CLI commands, guardiumATK gives you total programmatic control over your Guardium appliances.

Install `guardiumATK`:

- Clone or download the `guardiumATK` project.

- ```pip3 install -e /guardiumATK```

*Note: Manually installing the package through pip is temporary until an official PyPI package is made available.*

## Usage
Start by gathering your configuration details to be used when making CLI and REST API calls. This can be done in a 
configuration file ([config.yaml](/examples/config.yaml)) or a python dictionary 
([example here](/examples/rest_api_get_report_as_json.py)).

To use Guardium REST API functions: import and create an instance of `GuardiumRESTAPI` class.
```
>>> from guardiumATK import rest_api_functions
>>> guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="/guardiumATK/examples/test_config.yaml")
>>> result = guardium_api.get_list_of_policy_rules(params={'policy': 'Basic Data Security Policy', 'api_target_host': ''})
```

To use Guardium CLI functions: import and create an instance of `GuardiumCLI` class.
```
>>> from guardiumATK import cli_functions
>>> guardium_cli = cli_functions.GuardiumCLI(display=True, config_yaml_path="/guardiumATK/examples/test_config.yaml")
>>> result = guardium_cli.get_appliance_type()
```

To see more examples, visit the [examples](/examples) directory.
 
## Discussion
File bugs using the [issue tracker](https://github.com/jklahn/guardiumATK/issues).

Need help? Reach out to us on the
[Guardium community](https://community.ibm.com/community/user/groups/community-home?CommunityKey=aa1a6549-4b51-421a-9c67-6dd41e65ef85).


