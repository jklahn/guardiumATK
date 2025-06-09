from guardiumATK import cli_functions

"""

The following code creates an instance of Guardium CLI over SSH, using Paramiko. The code allows for using a proxy SSH
server if needed (this is configured in the config.yaml). Paramiko-expect is then leveraged to run CLI commands and wait
for the right output on the command line before proceeding. This example uses the 'store_remotelog' to add a remote
syslog integration to a Guardium appliance.

Reference: 
https://www.ibm.com/docs/en/gdp/12.x?topic=commands-configuration-control-cli#concept_dgk_2cj_4lb__store_remotelog
"""
# creates a CLI connection based on settings in the config.yaml
guardium_cli = cli_functions.GuardiumCLI(display=True, config_yaml_path="./test_config.yaml")
result = guardium_cli.get_appliance_type()
print("Appliance type is: " + result)
