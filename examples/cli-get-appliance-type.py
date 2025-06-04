from guardiumATK.cli_functions import GuardiumCLI

"""

The following code creates an instance of Guardium CLI over SSH, using Paramiko. The code allows for using a proxy SSH
server if needed (this is configured in the config.yaml). Paramiko-expect is then leveraged to run CLI commands and wait
for the right output on the command line before proceeding. Things are tricky in the CLI because you're dealing with 
inconsistent responses. Be wary of hidden characters. Use tools like .strip() to remove whitespace characters.

"""
# creates a CLI connection based on settings in the config.yaml
guardium_cli = GuardiumCLI(display=True)
result = guardium_cli.get_appliance_type()
print("Appliance type is: \n" + result)
