from guardiumATK.rest_api_functions import GuardiumRESTAPI

"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'rule_action' REST API is used to add an action
to an existing policy rule.

Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=reference-create-rule-action
Policy API commands: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-policy-rule-apis
"""


guardium_api = GuardiumRESTAPI(config_yaml_path="./test_config.yaml")

# Example: Add action to existing policy rule
result = guardium_api.post_policy_rule_action(params={
    'fromPolicy': '-JoshTestPolicy',  # str; required -- policy name
    'ruleDesc': 'Log DML',  # str; required -- rule name, Example: 'SQL Error - Log'
    'actionName': 'LOG FULL DETAILS PER SESSION',  # str; required - Example: 'LOG FULL DETAILS PER SESSION'
    'actionLevel': '',  # str;
    'actionParameters': '',  # str;
    'alertUserLoginName': '',  # str;
    'classDestination': '',  # str;
    'messageTemplate': '',  # str; -- Examples: Default, LEEF
    'notificationType': '',  # str; -- Examples: MAIL, SYSLOG, SNMP
    'paramSeparator': ''  # str;
            })

print(result)
