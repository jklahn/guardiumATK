from guardiumATK import rest_api_functions
import pandas
"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'online_report' REST API is used to fetch the
first 20 rows from the past 30 days of the report. The API returns a list of dictionaries - each representing a row in 
the report. Pandas is then used to make it look pretty in a tabular format.

"""
guardium_api = rest_api_functions.GuardiumRESTAPI(config_yaml_path="./test_config.yaml")
"""configs can also be passed as a dictionary, example:

config_dict={
    'api': {
            'guardium-api-url': 'https://guard.gdemo.com:8443',
             'oauth-client-id': 'client1',
             'oauth-client-secret': '81399384-6351-46fd-9cb3-ea7c2501cce3', 
             'guardium-admin-username': 'admin', 
             'guardium-admin-password': 'admin password here'}, 
     'cli': {
            'guardium-cli-hostname': 'guard.gdemo.com',
            'guardium-cli-port': '22',
            'guardium-cli-username': 'cli', 
            'guardium-cli-password': 'cli password here', 
            'ssh-proxy': 
                {'enabled': 'True', 
                'ssh-proxy-hostname': 'proxy.example.com', 
                'ssh-proxy-port': '20755', 
                'ssh-proxy-username': 'proxy username here', 
                'ssh-proxy-password': 'proxy ssh password here'}
            }
    }
"""

# Example: Running a report using 'online_report' API and making the results look pretty
result = guardium_api.post_online_report(params={
    'reportName': 'Sessions',
    'indexFrom': 1,
    'fetchSize': 20,
    'sortColumn': '',
    'sortType': '',
    'reportParameter': {
        'QUERY_FROM_DATE': 'NOW -30 DAY',
        'QUERY_TO_DATE': 'NOW',
        'SHOW_ALIASES': 'TRUE',
        'DBUser': '%',
        'REMOTE_SOURCE': '',
        'HostnameLike': '%',
        'hostLike': ''
    }
})

# converts the list of dictionaries into a pretty table
print(pandas.DataFrame(result))
