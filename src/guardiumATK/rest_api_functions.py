"""

A library of REST API functions that can be used with a valid GuardiumAPIConnection class

"""

from requests import get, post
from guardiumATK import appliance_connections_creator
import logging


def check_for_response_errors(result):

    valid_codes = [
        '200',  # RESPONSE_CODE_SUCCESS
        '<Response [200]>',  # RESPONSE_HTTP_SUCCESS
        '201',  # RESPONSE_CODE_SUCCESS_CREATED
        '202',  # RESPONSE_CODE_SUCCESS_ACCEPTED
        '204'   # RESPONSE_CODE_SUCCESS_NO_CONTENT
    ]

    if str(result) not in valid_codes:
        logging.error(Exception(result.text))
        raise


class GuardiumRESTAPI:
    """

    A class that allow streamlined execution of Guardium REST APIs

    """

    def __init__(self, config_yaml_path=None, config_dict=None):

        # Starts a valid REST API session
        self.guard_api = appliance_connections_creator.GuardiumAPIConnection(config_yaml_path=config_yaml_path, config_dict=config_dict)

    def get_list_parameter_names_by_report_name(self, params, verify=False, timeout=None):
        """

        :param params: reportName
        :param verify: verifies the SSL connection
        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :return: response: as JSON
        """

        response = get(url=self.guard_api.host_url + '/restAPI/' + 'list_parameter_names_by_report_name',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       params=params,
                       timeout=timeout)  # Example {'reportName': 'Sessions'}

        check_for_response_errors(response)

        return response.json()

    def post_online_report(self, params, verify=False, timeout=None):
        """

        :param params: as JSON dictionary
            "reportName": reportName -- [required] the name of the required report
            "indexFrom": indexFrom -- an integer of the starting index for the first record to be retrieved in the
                current fetch operation. To fetch subsequent parts of the data, increment the offset by the previous
                fetch size. Index starts at '1' (not '0')
            "fetchSize": fetchSize -- an integer of number of rows returned for a report. Default is 20 rows.
            "sortColumn": sortColumn
            "sortType": sortType
            "reportParameter": report_parameters -- additional (nested) JSON dictionary using the parameters below:
                "QUERY_FROM_DATE": query_from_date -- from what date to start query, e.g. : NOW -10 DAY
                "QUERY_TO_DATE": query_to_date -- until what day to start query, e.g. : NOW
                "SHOW_ALIASES": show_aliases -- Boolean - 'TRUE' or 'FALSE'
                "DBUser": db_user_name
                "REMOTE_SOURCE": remote_source
                "HostnameLike": host_name_like
                "hostLike": host_name_like
        :param verify: verifies the SSL connection
        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """

        response = post(url=self.guard_api.host_url + '/restAPI/' + 'online_report',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_policy_rule_action(self, params, verify=False, timeout=None):
        """
        Creates a policy rule action

        :param params: as JSON dictionary

            params={
                'fromPolicy': 'Basic Data Security Policy',  # str; required -- policy name
                'ruleDesc': '',  # str; required -- rule name, Example: 'Failed Login - Log Violation'
                'actionName': 'LOG FULL DETAILS PER SESSION',  # str; required - Examples:
                # 'LOG ONLY', 'LOG FULL DETAILS PER SESSION', 'ALERT DAILY', 'IGNORE S-TAP SESSION'
                'actionLevel': '',  # str;
                'actionParameters': '',  # str;
                'alertUserLoginName': '',  # str;
                'classDestination': '',  # str;
                'messageTemplate': '',  # str; -- Examples: Default, LEEF
                'notificationType': '',  # str; -- Examples: MAIL, SYSLOG, SNMP
                'paramSeparator': ''  # str;
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'rule_action',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def get_list_of_policies(self, params, verify=False, timeout=None):
        """
        Displays a list of available policies or displays details about a single policy.

        :param params: as JSON dictionary

            params={
                'detail': 1,  # [int]; Display details about a policy (or all policies if you do not specify a
                    # policyDesc). Valid values: 0(false),1 (true)
                'policyDesc': '',  # [str] -- The name of one policy to display. If not specified, Guardium returns
                    # information about all available policies.
                'verbose': 0,  # [int] -- 0(false),1 (true)
                'api_target_host': '',  # str; Specifies the target hosts where the API executes
                    # 'all_managed': execute on all managed units but not the central manager
                    # 'all': execute on all managed units and the central manager
                    # 'group:<group name>': execute on all managed units identified by <group name>
                    #  host name or IP address of the central manager. Example, api_target_host=10.0.1.123
            }

        :param verify: verifies the SSL connection
        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :return: response: as JSON
        """

        response = get(url=self.guard_api.host_url + '/restAPI/' + 'policy',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       params=params,  # Example {'reportName': 'Sessions'}
                       timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def get_list_of_policy_rules(self, params, verify=False, timeout=None):
        """
        Displays a list of rules for a given policy

        :param params: as JSON dictionary

            params={
                'policy': '',  # [str][required]; Name of the policy
                'api_target_host': ''  # [str]; host name or IP address of the central manager
            }

        :param verify: verifies the SSL connection
        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :return: response: as JSON
        """

        response = get(url=self.guard_api.host_url + '/restAPI/' + 'rule',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       params=params,  # Example {'reportName': 'Sessions'}
                       timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def get_list_of_policy_rules_detailed(self, params, verify=False, timeout=None):
        """
        Displays a list of rules for a given policy and includes ALL the details - like actions and continueToNextRule

        :param params: as JSON dictionary

            params={
                'policyDesc': '',  # [str][required]; Name of the policy
                'api_target_host': ''  # [str]; host name or IP address of the central manager
                'localeLanguage': 0  # [int]; 0 (false), 1 (true)
            }

        :param verify: verifies the SSL connection
        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :return: response: as JSON
        """

        response = get(url=self.guard_api.host_url + '/restAPI/' + 'ruleInfoFromPolicy',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       params=params,  # Example {'reportName': 'Sessions'}
                       timeout=timeout)

        check_for_response_errors(response)

        return response.json()
