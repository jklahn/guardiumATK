from guardiumATK.rest_api_functions import GuardiumRESTAPI
import pandas
"""

The following code creates an instance Guardium REST API - which comes with an access token and REST API functions based 
on what is in 'guardium_rest_api_functions' module. In this example, the 'online_report' REST API is used to fetch the
first 20 rows from the past 30 days of the report. The API returns a list of dictionaries - each representing a row in 
the report. Pandas is then used to make it look pretty in a tabular format.

"""
guardium_api = GuardiumRESTAPI()

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
