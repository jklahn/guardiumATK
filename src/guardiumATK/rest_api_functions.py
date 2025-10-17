"""

A library of REST API functions that can be used with a valid GuardiumAPIConnection class

"""

from requests import get, post, delete
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

    def post_create_policy(self, params, verify=False, timeout=None):
        """
        Creates a new policy

        :param params: as JSON dictionary

            params={
                'ruleSetDesc': '-ChuckWasHere',  # [str][required]; -- The name of the policy to be created.
                'baselineDesc': '',  # [str];
                'categoryName': '',  # [str]; -- Category of the policy, Example: 'Access', 'Activity', 'SOX'
                'isFam': None,  # [boolean]; -- Determines whether policy is for file access monitoring. Valid values:
                                # 0 (false): This is a data access monitoring policy.
                                # 1 (true): This is a file access monitoring policy.
                'logFlat': '',  # [boolean]; -- Flat logging option for this policy. Valid values:
                                # 0 (false)
                                # 1 (true)
                'pattern': '',  # [str]; -- A regular expression to match.
                'policyLevel': '',  # [str]; -- REGULAR [DEFAULT], SESSION, FAM, FAM_SP, FAM_NAS, 0, 1, 2, 3, 4
                'rulesOnFlat': None,  # [boolean]; -- Valid values: 0 (false)[DEFAULT], 1 (true)
                'securityPolicy': None,  # [boolean]; -- Valid values: 0 (false)[DEFAULT], 1 (true)
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'policy',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_add_rule_to_policy(self, params, verify=False, timeout=None):
        """
        Creates a new policy

        :param params: as JSON dictionary

            params={
                'fromPolicy': '',  # [str] [required]; -- Policy name to add the rule to
                'ruleType': '',  # [str] [required]; -- ACCESS, EXCEPTION, EXTRUSION, MASK_ON_SCREEN,
                    # MASK_ON_DB, MASK_ON_MONGODB, DATASET_COLLECTION_PROFILE, DB2_COLLECTION_PROFILE,
                    # DB2_BLOCKING_PROFILE, IMS_COLLECTION_PROFILE, SESSION
                'category': '',  # [str]; -- Access, Activity, Audit, Audit Mode, BASEL II, CCPA, Data Privacy...
                'classification': '',  # [str];
                'order': '',  # [int];
                'ruleDesc': '',  # [str] [required]; -- Unique name for the rule
                'ruleLevel': '',  # [str];
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'rule',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_install_policy(self, params, verify=False, timeout=None):
        """
        Installs a policy

        :param params: as JSON dictionary

            params={
                'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy or policies to install
                                            # Use a pipe ( | ) character to separate multiple policies
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'policy_install',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_uninstall_policy(self, params, verify=False, timeout=None):
        """
        Uninstalls a policy

        :param params: as JSON dictionary

            params={
                'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy to uninstall
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'policy_uninstall',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_reinstall_policy(self, params, verify=False, timeout=None):
        """
        Re-installs an existing policy to implement changes

        :param params: as JSON dictionary

            params={
                'policy': '-ChuckWasHere',  # [str] [required]; -- The name of the policy to re-install
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'reinstall_policy',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def delete_policy(self, params, verify=False, timeout=None):
        """
        Deletes an existing policy

        :param params: as JSON dictionary

            params={
                'policyDesc': '-ChuckWasHere',  # [str][required]; -- The name of the policy to be deleted.
                'api_target_host': ''  # [str]; -- Specifies the target hosts where the API executes
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing DELETE...")
        response = delete(url=self.guard_api.host_url + '/restAPI/' + 'policy',
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

    def post_create_group(self, params, verify=False, timeout=None):
        """
        Creates a group

        :param params: as JSON dictionary

            params={
                'appid': 'Public',  # [str] [required]; -- Example: Public, Classifier, Policy Builder
                'category': '',  # [str]; -- optional label that is used to group policy violations for reporting
                'classification': '',  # [str]; -- optional label that is used to group policy violations for reporting
                'desc': 'My Custom User Group',  # [str] [required]; -- a unique description for the new group
                'hierarchical': '',  # [str]; -- true/false; indicates if the group is meant to contain other
                    groups (hierarchical)
                'tuple_parameters': '',  # [str]; -- if group type is 'Tuples', use a comma separated list of tuple
                    parameters to define the tuple. Valid parameters: client_ip, client_host_name, server_ip,
                    server_host_name, source_program, db_name, db_user, service_name, app_user_name, os_user, db_type,
                    net_protocol, command, server_port, sender_ip, server_description, analyzed_client_ip, incident,
                    session, client_os_name, server_os_name, db_prototype, field_name, error_code
                'type': 'USERS'  # [str] [required]; -- type of group. Examples: COMMANDS, Database Name, OBJECTS, USERS
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'group',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def get_group_members_by_desc(self, params, verify=False, timeout=None):
        """
        Gets the list the members of a group, using the group name as the identifier

        :param params: as JSON dictionary

            params={
                'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to list the members
                'api_target_host': '%CREDIT'  # [str]; -- Specifies the target hosts where the API executes. Examples:
                    'all_managed': execute on all managed units but not the central manager
                    'all': execute on all managed units and the central manager
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing GET...")
        response = get(url=self.guard_api.host_url + '/restAPI/' + 'group_members_by_group_desc',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       json=params,
                       timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def delete_group_by_desc(self, params, verify=False, timeout=None):
        """
        Deletes a group using the name of the group as the identifier

        :param params: as JSON dictionary

            params={
                'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to be deleted
                'api_target_host': '%CREDIT'  # [str]; -- Specifies the target hosts where the API executes. Examples:
                    'all_managed': execute on all managed units but not the central manager
                    'all': execute on all managed units and the central manager
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing DELETE...")
        response = delete(url=self.guard_api.host_url + '/restAPI/' + 'group',
                          headers={'Content-Type': 'application/json',
                                   'Authorization': 'Bearer ' + self.guard_api.access_token},
                          verify=verify,
                          json=params,
                          timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def post_add_member_to_group_by_desc(self, params, verify=False, timeout=None):
        """
        Adds a member to an existing group identified by its description.

        :param params: as JSON dictionary

            params={
                'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to add the member to
                'member': '%CREDIT'  # [str] [required]; -- The member name (must be unique within the group)
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing POST...")
        response = post(url=self.guard_api.host_url + '/restAPI/' + 'group_member',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params,
                        timeout=timeout)

        check_for_response_errors(response)

        return response.json()

    def delete_member_from_group_by_desc(self, params, verify=False, timeout=None):
        """
        Removes a member from an existing group identified by its description.

        :param params: as JSON dictionary

            params={
                'desc': 'Sensitive Objects',  # [str] [required]; -- The name of the group to remove the member from
                'member': '%CREDIT',  # [str] [required]; -- The member name (must be unique within the group)
                'api_target_host': '%CREDIT'  # [str]; -- Specifies the target hosts where the API executes. Examples:
                    'all_managed': execute on all managed units but not the central manager
                    'all': execute on all managed units and the central manager
            }

        :param timeout: [int] number of seconds Requests will wait for your client to establish a connection
        :param verify: verifies the SSL connection
        :return: response: a list of dictionaries, where each dictionary represents a row

        """
        print("Performing DELETE...")
        response = delete(url=self.guard_api.host_url + '/restAPI/' + 'group_member',
                          headers={'Content-Type': 'application/json',
                                   'Authorization': 'Bearer ' + self.guard_api.access_token},
                          verify=verify,
                          json=params,
                          timeout=timeout)

        check_for_response_errors(response)

        return response.json()
