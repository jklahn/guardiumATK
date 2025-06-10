from json import loads
from requests import post
import yaml
from paramiko import SSHClient, AutoAddPolicy, SSHException
import logging
from time import sleep

# set global dictionary used for storing imported configurations
imported_configs = {}


def import_config(config_yaml_path, config_dict):

    global imported_configs

    # If using config.yaml, attempt import configuration from yaml
    if config_yaml_path:

        with open(config_yaml_path, "r") as config_file:
            """
            Opens the config.yaml and turns it into a dictionary so key/value pairs can be read later on.
            """
            try:
                imported_configs = yaml.safe_load(config_file)
                logging.info('Successfully opened config.yaml.')

            except yaml.YAMLError as exc:
                logging.critical(Exception('Failed to load configurations from config.yaml file', exc))

    elif config_dict:
        imported_configs = config_dict

    else:
        logging.critical(Exception('Configuration was not passed. Supply a path to the config.yaml or pass the config'
                                   'as a python dictionary'))


class GuardiumAPIConnection:
    """

    A class that represent an API connection to a Guardium Appliance

    Attributes
    -------------
    host_url: hostname of the Guardium appliance
    access_token: temporary access token used to grant access for using Guardium APIs

    """

    host_url = ''
    access_token = ''

    def __init__(self, config_yaml_path=None, config_dict=None):
        """

        Uses the values from config.yaml file to connect to a guardium appliance and get an access token

        """

        import_config(config_yaml_path=config_yaml_path, config_dict=config_dict)

        global imported_configs

        self.host_url = imported_configs['api']['guardium-api-url']
        guardium_oauth_client_id = imported_configs['api']['oauth-client-id']
        guardium_oauth_client_secret = imported_configs['api']['oauth-client-secret']
        guardium_admin_user = imported_configs['api']['guardium-admin-username']
        guardium_admin_password = imported_configs['api']['guardium-admin-password']

        logging.info('Successfully set API values based on config.yaml.')

        # the /oauth/token expects a string with all the oAuth client information combined
        oauth_data: str = ("client_id=" + guardium_oauth_client_id +
                           "&client_secret=" + guardium_oauth_client_secret +
                           "&grant_type=password&username=" + guardium_admin_user +
                           "&password=" + guardium_admin_password)

        response = post(url=self.host_url + '/oauth/token',
                        data=str(oauth_data),
                        verify=False,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        timeout=30)

        logging.info('Getting API access token from ' + self.host_url + '/oauth/token')

        if response.status_code != 200:
            logging.critical(
                Exception("Error generating the access token needed as part of oAuth: " + response.text,
                          response.status_code))
            raise

        else:
            response_json = loads(response.text)  # converts the response into JSON
            self.access_token = response_json["access_token"]  # access token used for API auth
            logging.info('Successfully fetched API access token.')


class GuardCLIConnection:
    """

    Makes a class that represents the Guardium CLI

    """
    guardium_cli = None  # SSH instance to the Guardium CLI for running CLI commands
    is_proxy_ssh_active = False
    display = False

    def __init__(self, missing_host_key_policy=True, display=False, config_yaml_path=None, config_dict=None):

        import_config(config_yaml_path=config_yaml_path, config_dict=config_dict)

        global imported_configs
        self.display = display

        # Fetch the values from config.yaml
        cli_hostname = imported_configs['cli']['guardium-cli-hostname']
        cli_port = imported_configs['cli']['guardium-cli-port']
        cli_username = imported_configs['cli']['guardium-cli-username']
        cli_password = imported_configs['cli']['guardium-cli-password']

        # If using a proxy SSH to get to Guardium CLI
        if imported_configs['cli']['ssh-proxy']['enabled'] == 'True':

            # Get the proxy values from config.yaml
            ssh_proxy_hostname = imported_configs['cli']['ssh-proxy']['ssh-proxy-hostname']
            ssh_proxy_port = imported_configs['cli']['ssh-proxy']['ssh-proxy-port']
            ssh_proxy_username = imported_configs['cli']['ssh-proxy']['ssh-proxy-username']
            ssh_proxy_password = imported_configs['cli']['ssh-proxy']['ssh-proxy-password']

            # Make an SSH connection to the proxy
            try:
                proxy_ssh = SSHClient()
                if missing_host_key_policy:
                    proxy_ssh.set_missing_host_key_policy(AutoAddPolicy())

                proxy_ssh.connect(hostname=ssh_proxy_hostname,
                                  port=int(ssh_proxy_port),
                                  username=ssh_proxy_username,
                                  password=ssh_proxy_password)

                self.is_proxy_ssh_active = proxy_ssh.get_transport().is_active()
                if self.is_proxy_ssh_active:
                    logging.info("Connected to the proxy.")
                    if self.display:
                        print("Connected to the proxy.")

                # prepare for proxying the SSH connection to the Guardium CLI by opening a new channel locally
                ssh_proxy_transport = proxy_ssh.get_transport()

                # tuples for the connection settings
                dest_addr = (cli_hostname, int(cli_port))
                src_addr = (ssh_proxy_hostname, int(ssh_proxy_port))
                # open the channel
                cli_ssh_channel = ssh_proxy_transport.open_channel('direct-tcpip',
                                                                   dest_addr=dest_addr,
                                                                   src_addr=src_addr)

                # Use the channel for SSH connect to Guardium CLI
                ssh_cli = SSHClient()
                ssh_cli.set_missing_host_key_policy(AutoAddPolicy())
                ssh_cli.connect(hostname=cli_hostname,
                                port=cli_port,
                                username=cli_username,
                                password=cli_password,
                                sock=cli_ssh_channel)

                # set the instance for the class
                self.guardium_cli = ssh_cli.invoke_shell()
                # self.guardium_cli.set_combine_stderr(True)  # combine stdout and stderr on this channel

                # wait for the CLI to start printing initial login messages
                while not self.guardium_cli.recv_ready():
                    sleep(.5)

                logging.info("Connected through proxy to the CLI")
                if self.display:
                    print("Connected through proxy to the CLI.")

                # get the initial CLI login text read
                output = self.guardium_cli.recv(10000).decode("utf-8")  # grabs last 10MB since the cmd was run

                countdown = 30
                while '>' not in output or countdown <= 0:
                    if self.display:
                        print(output)
                    sleep(.5)
                    countdown -= 1
                    output = self.guardium_cli.recv(10000).decode("utf-8")  # grabs last 10MB since the cmd was run

                # CLI is ready
                logging.info("CLI is ready for commands.")
                if self.display:
                    print("CLI is ready for commands.")

            except SSHException as e:
                Exception("Error making SSH proxy connection", e)

        else:  # Not using a proxy - connect directly to CLI
            ssh_cli = SSHClient()
            ssh_cli.set_missing_host_key_policy(AutoAddPolicy())
            ssh_cli.connect(hostname=cli_hostname,
                            port=cli_port,
                            username=cli_username,
                            password=cli_password,
                            sock=None)

            # set the instance for the class
            self.guardium_cli = ssh_cli.invoke_shell()
            # self.guardium_cli.set_combine_stderr(True)  # combine stdout and stderr on this channel

            # wait for the CLI to start printing initial login messages
            while not self.guardium_cli.recv_ready():
                sleep(.5)

            logging.info("Connected through proxy to the CLI")
            if self.display:
                print("Connected through proxy to the CLI.")

            # get the initial CLI login text read
            while self.guardium_cli.recv_ready():
                output = self.guardium_cli.recv(10000).decode("utf-8")  # grabs last 10MB since the cmd was run
                if self.display:
                    print(output)
                sleep(.5)

            logging.info("CLI is ready for commands.")
            if self.display:
                print("CLI is ready for commands.")

    def close_cli(self):

        # close the CLI
        # self.guardium_cli.exec_command('quit')

        # close the SSH session
        self.guardium_cli.close()

    def run_cli_cmd(self, cli_cmd, strs_to_match_in_output, timeout_counter=30, sleep_time_increment=0.5,
                    enter_key='\n'):
        """

        :param cli_cmd: CLI command to run. Do not include the enter key.
        :param strs_to_match_in_output: List of strings. If any match, it shows the command completed
        :param timeout_counter: Time to wait before giving up on the command to complete (seconds)
        :param sleep_time_increment: How long to wait before checking if the command completed
        :param enter_key: character that submits the command
        :return:
        """

        timeout_counter = timeout_counter
        accumulated_output = ''

        logging.info("Running CLI command: '" + cli_cmd + "'")
        if self.display:
            print("\nRunning CLI command: " + cli_cmd + "\n")

        self.guardium_cli.send(cli_cmd + enter_key)  # Send the command to the CLI, followed by the enter key
        sleep(sleep_time_increment)

        while timeout_counter > 0:

            # something is ready to be read
            if self.guardium_cli.recv_ready():
                output = self.guardium_cli.recv(10000).decode("utf-8")  # grabs last 10MB since the cmd was run
                if self.display:
                    print(output)

                for string in strs_to_match_in_output:
                    if string in output:
                        accumulated_output += output
                        return accumulated_output  # match string found, command completed, leave the loop

                else:
                    accumulated_output += output  # append the difference to the accumulated string

            sleep(sleep_time_increment)
            timeout_counter -= sleep_time_increment  # count down by the sleep time increment

        # Timeout exceeded. Throw an error and log it. Return the output that happened while waiting
        logging.error(Exception(str(timeout_counter) + " timeout counter exceeded while waiting for '" + cli_cmd +
                                "' CLI command to complete."))

        return accumulated_output
