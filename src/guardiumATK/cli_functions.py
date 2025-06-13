import logging
from guardiumATK import appliance_connections_creator
from re import compile

"""

A library of Guardium CLI functions that can be used with a valid GuardCLIConnection class

"""


def check_for_cli_errors(cmd, result, success_str='ok', error_str=None):
    """

    :param cmd: [required][str] -- Command being run. Used for context in error message.
    :param result: [required][str] -- Output from running the command
    :param success_str: [optional][str] -- String to match when confirming successful command execution. Default is 'ok'
    :param error_str: [optional][str] -- String to match when looking for failure of a command.

    """

    # check for error first
    if error_str:
        if error_str in result:
            logging.error(Exception("Failed running Guardium CLI command: '" + cmd + "'; "
                                    + error_str, result))
            return

    # check for success
    if success_str not in result:  # CLI commands that execute successfully typically have the last line 'ok'
        logging.error(Exception("Failed running Guardium CLI command: '" + cmd + "'", result))


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

    def add_remote_syslog(self, params, clear_existing=False):
        """

        Adds a remote syslog integration so that Guardium can send messages to it such as policy alerts and audit logs

        :param params: [required][dict] -- IP address that will have access to the file server
        {
            'encryption': 'encrypted' | 'non_encrypted',  # determines if the outgoing messages are encrypted
            'facility': 'daemon' | 'user', [audit logs]  # syslog source and topic
            # outgoing message filtering
            priority: 'all' | 'alert' [Guardium 'HIGH'] | 'crit' | 'debug' | 'emerg' | 'err' [Guardium 'MED'] |
            'info' [Guardium INFO] | 'notice' | 'warning' [Guardium LOW]  # syslog message priority (urgency),
            'host': 'destination rsyslog server',  # [str][required] -- hostname or IP address
            'port': 'port number', # [str][optional] -- default 514
            'protocol': 'tcp' | 'udp',  # [str] Only TCP support encryption; TCP is recommended for large message
                payload.
            'format': 'default' | 'rfc5424',  # [str][optional]  message format
            'escape_control_characters': 'on' | 'off'.  # [str][optional] escape the control characters if your system
                mangles messages that include control characters
            'max_message_size' | '1'  # [optional][5k] | '2' [10k]| '3' [15k] | '4' [20k]| '5' [23k] | '6' [64k],
            'public_cert_pem' | 'pem_str',  # [str] public CA certificate (.pem) from the rsyslog receiver
        }

        :param clear_existing: [boolean] -- Clears existing 'facility.priority' combination from the specified host (in params)
        first before adding the new one

        References:
            https://www.ibm.com/docs/en/gdp/12.x?topic=commands-configuration-control-cli#concept_dgk_2cj_4lb__store_remotelog
            https://www.ibm.com/docs/en/gdp/12.x?topic=system-facility-priority-syslog-messages

        Example command: store remotelog add encrypted user.info 9.30.252.111 tcp

        """

        # Use port 514 if none specified
        if params['port'] == '':
            port = ''
        else:
            port = ':' + params['port']

        if clear_existing:

            # clear the facility.priority combo for the host first
            command = 'store remotelog clear {host}'.format(host=params['host'])

            self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['>'])

        # prepare command for adding rsyslog
        command = 'store remotelog add {encrypted} {facility}.{priority} {host}{port} {protocol} {format}'.format(
            encrypted=params['encryption'],
            facility=params['facility'],
            priority=params['priority'],
            host=params['host'],
            port=port,
            protocol=params['protocol'],
            format=params['format']
        )

        # using encryption, so the command execution is different
        if params['encryption'] == 'encrypted':

            self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['Please paste your CA certificate'])

            # send the pem string
            result = self.guard_cli.run_cli_cmd(cli_cmd=params['public_cert_pem'],
                                                strs_to_match_in_output=['>'],
                                                enter_key='\x04')  # CTRL-D

            check_for_cli_errors(cmd=command, result=result,
                                 success_str='Certificate passed validation',
                                 error_str='Unable to load certificate')

        else:  # not encrypted

            # Example: store remotelog add non_encrypted user.all raptor.gdemo.com:514 tcp default

            result = self.guard_cli.run_cli_cmd(cli_cmd=command,
                                                strs_to_match_in_output=['>'])

            check_for_cli_errors(cmd=command, result=result, success_str='ok')

            """
            
            Example result:
    
                tcp forwarder to raptor.gdemo.com:514 added to rsyslog configuration:
                user.*    @@raptor.gdemo.com:514
                
                Restarting remote logger...
                Remote logger restarted successfully
                Command ran on: Tue Jun 10 14:44:28 2025
                ok
    
            """

        # set message size if the parameter is present
        if params['max_message_size']:
            # store remotelog max_message_size <1|2|3|4|5|6>
            command = 'store remotelog max_message_size {size}'.format(size=params['max_message_size'])

            result = self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['>'])

            check_for_cli_errors(cmd=command, result=result, success_str='Configuration changed')

        # set to escape (add a '/') the control characters of outgoing messages
        if params['escape_control_characters']:
            # store remotelog escape_control_characters_on_receive <on|off>
            command = ('store remotelog escape_control_characters_on_receive {setting}'.format
                       (setting=params['escape_control_characters']))
            self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['>'])

        """
        Example output:
        
            store remotelog escape_control_characters_on_receive off
            Configuration changed. Run 'restart remotelog' to apply.
            Command ran on: Wed Jun 11 17:27:05 2025
            ok
        
        Example output if already set:
        
            store remotelog escape_control_characters_on_receive off
            Escape control characters is already off
            Command ran on: Wed Jun 11 17:31:55 2025
            ok
            
        """

        # test rsyslog config by sending a test message and observing it in the tcpdump output
        if params['send_test_msg']:
            # store remotelog max_message_size <1|2|3|4|5|6>
            command = 'show remotelog test'

            # tests can take a while, so increasing timeout counter to 120
            result = self.guard_cli.run_cli_cmd(cli_cmd=command, strs_to_match_in_output=['>'], timeout_counter=120)

            """
            Example output:
            
                show remotelog test
                
                Remote log receivers are configured.
                Messages will be written to syslog targeting these
                   - for facility 'ALL', 'daemon' is used for testing.
                   - Messages of 'kern' facility cannot be tested
                   - for priority 'ALL', 'info' is used for testing.
                
                The tests could take several minutes... Please wait
                
                Testing raptor.gdemo.com:514/tcp for user.debug
                Got response from raptor.gdemo.com:514/tcp for user.debug
                Testing raptor.gdemo.com:514/tcp for user.info
                Got response from raptor.gdemo.com:514/tcp for user.info
                ...
                OK:  raptor.gdemo.com:514/tcp for user.*
                ok
            """

            check_for_cli_errors(cmd=command, result=result, success_str='ok')

        return 'Successfully added remote syslog.'
