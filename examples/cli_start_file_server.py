from guardiumATK import cli_functions

"""

The following code creates an instance of Guardium CLI over SSH, using Paramiko. The code allows for using a proxy SSH
server if needed (this is configured in the config.yaml). Paramiko-expect is then leveraged to run CLI commands and wait
for the right output on the command line before proceeding. Things are tricky in the CLI because you're dealing with 
inconsistent responses. Be wary of hidden characters. Use tools like .strip() to remove whitespace characters.

Reference: 
https://www.ibm.com/docs/en/gdp/12.x?topic=commands-file-handling-cli#file_handling_cli_commands__Fileserver__title__1

"""
# creates a CLI connection based on settings in the config.yaml
guardium_cli = cli_functions.GuardiumCLI(display=True, config_yaml_path="./test_config.yaml")

# starts the file server using the CLI command: 'fileserver {ip} {timeout}'
result = guardium_cli.start_fileserver(client_ip_address='192.168.1.10', timeout=3600)
print(result)
