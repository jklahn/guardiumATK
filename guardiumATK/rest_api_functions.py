"""

A library of REST API functions that can be used with a valid GuardiumAPIConnection class

"""

from requests import get, post
from appliance_connections_creator import GuardiumAPIConnection
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

    def __init__(self):
        # Starts a valid REST API session by getting an access token using settings in config.yaml file
        self.guard_api = GuardiumAPIConnection()

    def get_list_parameter_names_by_report_name(self, params, verify=False):
        """

        :param params: reportName
        :param verify: verifies the SSL connection
        :return: response: as JSON
        """

        response = get(url=self.guard_api.host_url + '/restAPI/' + 'list_parameter_names_by_report_name',
                       headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + self.guard_api.access_token},
                       verify=verify,
                       params=params)  # Example {'reportName': 'Sessions'}

        check_for_response_errors(response)

        return response.json()

    def post_online_report(self, params, verify=False):
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
        :return: response: a list of dictionaries, where each dictionary represents a row

        """

        response = post(url=self.guard_api.host_url + '/restAPI/' + 'online_report',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + self.guard_api.access_token},
                        verify=verify,
                        json=params)

        check_for_response_errors(response)

        return response.json()
