import logging
from guardiumATK import appliance_connections_creator
from re import compile

"""

A library of Guardium CLI functions that can be used with a valid GuardCLIConnection class

"""


def check_for_cli_errors(cmd, result, success_str='ok'):
    # Get the last night to determine result of the command. 'err' or 'ok'

    if success_str not in result:  # CLI commands that execute successfully typically have the last line 'ok'
        logging.error(Exception("Failed running Guardium CLI command '" + cmd + "'", result))


class GuardiumCLI:

    def __init__(self, display=False, config_yaml_path=None, config_dict=None):
        # Starts a valid CLI SSH session using settings in config.yaml file
        self.guard_cli = appliance_connections_creator.GuardCLIConnection(display=display,
                                                                          config_yaml_path=config_yaml_path,
                                                                          config_dict=config_dict)

    def get_appliance_type(self):
        """

        :return: [str] Appliance type - example 'Standalone Aggregator'

        """
        command = 'show unit type'
        result = self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['>'])

        """
        Example result:
        
            show unit type
            Standalone Netinsp stap  
            ok
            guard.gdemo.com>
            
        """

        check_for_cli_errors(cmd=command, result=result, success_str='ok')

        # cleaning up the result
        ansi_escape = compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')  # Getting rid of ansi escape characters

        result = ansi_escape.sub('', result)

        lines = []
        for line in result.splitlines():
            if line == '':
                pass
            else:
                newline = line.rstrip()  # ['show unit type', 'Standalone Netinsp stap', 'ok', 'guard.gdemo.com>']
                lines.append(newline)

        result = lines[1]  # return the second string in the list - 'Standalone Netinsp stap'

        return result

    def start_fileserver(self, client_ip_address, timeout=3600):
        """

        Starts a file server with a simple GUI for manually uploading patches to an appliance.

        :param client_ip_address: [required][str] -- IP address that will have access to the file server
        :param timeout: [required][int] -- Duration of time in seconds; range 60 (minimum) to 3600 (maximum)

        Reference: https://www.ibm.com/docs/en/gdp/12.x?topic=commands-file-handling-cli#file_handling_cli_commands__Fileserver__title__1

        """
        command = 'fileserver {ip} {timeout}'.format(ip=client_ip_address, timeout=timeout)
        result = self.guard_cli.run_cli_cmd(cli_cmd=command,
                                            strs_to_match_in_output=['The file server is ready', 'already running'])

        """
        Example result:
        
            Starting the file server...
            The file server is ready at https://guard.gdemo.com:8445
            The timeout has been set to 3600 seconds and it may timeout during the uploading.
            
            The upload will only be accessible from the IP you are logged in from: 192.168.1.10
            
            Press ENTER to stop the file server.

        """

        # check_for_cli_errors(cmd=command, result=result, success_str='ok') -- Not applicable

        return result
