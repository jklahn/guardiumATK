import logging
from appliance_connections_creator import GuardCLIConnection
from re import compile

"""

A library of Guardium CLI functions that can be used with a valid GuardCLIConnection class

"""


def check_for_cli_errors(cmd, result, success_str='ok'):
    # Get the last night to determine result of the command. 'err' or 'ok'

    if success_str not in result:  # CLI commands that execute successfully typically have the last line 'ok'
        logging.error(Exception("Failed running Guardium CLI command '" + cmd + "'", result))


class GuardiumCLI:

    def __init__(self, display=False):
        # Starts a valid CLI SSH session using settings in config.yaml file
        self.guard_cli = GuardCLIConnection(display=display)

    def get_appliance_type(self):
        """

        :return: [str] Appliance type - example 'Standalone Aggregator'

        """
        command = 'show unit type'
        result = self.guard_cli.run_cli_cmd(cli_cmd=command, str_to_match_in_output='>')

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
