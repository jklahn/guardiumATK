from guardiumATK import cli_functions

"""

The following code creates an instance of Guardium CLI over SSH, using Paramiko. The code allows for using a proxy SSH
server if needed (this is configured in the config.yaml). Paramiko-expect is then leveraged to run CLI commands and wait
for the right output on the command line before proceeding. This example uses the 'store_remotelog' to add a remote
syslog integration to a Guardium appliance.

References: 
https://www.ibm.com/docs/en/gdp/12.x?topic=commands-configuration-control-cli#concept_dgk_2cj_4lb__store_remotelog
https://www.ibm.com/docs/en/gdp/12.x?topic=system-facility-priority-syslog-messages
"""
# creates a CLI connection based on settings in the config.yaml
guardium_cli = cli_functions.GuardiumCLI(display=True, config_yaml_path="./test_config.yaml")

public_ca_pem = """
-----BEGIN CERTIFICATE-----
MIIECTCCA3KgAwIBAgIUDnU7Oa0fU9GFOwU7EWJP3HsRchEwDQYJKoZIhvcNAQEL
BQAwgZkxCzAJBgNVBAYTAlVTMRAwDgYDVQQIDAdNb250YW5hMRAwDgYDVQQHDAdC
b3plbWFuMREwDwYDVQQKDAhTYXd0b290aDEYMBYGA1UECwwPQ29uc3VsdGluZ18x
MDI0MRgwFgYDVQQDDA93d3cud29sZnNzbC5jb20xHzAdBgkqhkiG9w0BCQEWEGlu
Zm9Ad29sZnNzbC5jb20wHhcNMjIxMjE2MjExNzQ5WhcNMjUwOTExMjExNzQ5WjCB
mTELMAkGA1UEBhMCVVMxEDAOBgNVBAgMB01vbnRhbmExEDAOBgNVBAcMB0JvemVt
YW4xETAPBgNVBAoMCFNhd3Rvb3RoMRgwFgYDVQQLDA9Db25zdWx0aW5nXzEwMjQx
GDAWBgNVBAMMD3d3dy53b2xmc3NsLmNvbTEfMB0GCSqGSIb3DQEJARYQaW5mb0B3
b2xmc3NsLmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAzazdR+y+tyTD
YxtUmHnhxzEWWdadd52N4ovtBBeyxuvkm5G+MVBil1i1fynes3EkC7+XCX8m3C3s
qC6yZCt6KzUZLaKAy5n9lHEbI41U2y5ijYEILfQkcids+cmO20x1upsB+D8Y9OZ/
+1eUksyIxLQAwqrU5YgYsxEvc8DWKQkCAwEAAaOCAUowggFGMB0GA1UdDgQWBBTT
Io8oLOAF7tPtw3E9ybI2Oh2/qDCB2QYDVR0jBIHRMIHOgBTTIo8oLOAF7tPtw3E9
ybI2Oh2/qKGBn6SBnDCBmTELMAkGA1UEBhMCVVMxEDAOBgNVBAgMB01vbnRhbmEx
EDAOBgNVBAcMB0JvemVtYW4xETAPBgNVBAoMCFNhd3Rvb3RoMRgwFgYDVQQLDA9D
b25zdWx0aW5nXzEwMjQxGDAWBgNVBAMMD3d3dy53b2xmc3NsLmNvbTEfMB0GCSqG
SIb3DQEJARYQaW5mb0B3b2xmc3NsLmNvbYIUDnU7Oa0fU9GFOwU7EWJP3HsRchEw
DAYDVR0TBAUwAwEB/zAcBgNVHREEFTATggtleGFtcGxlLmNvbYcEfwAAATAdBgNV
HSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDQYJKoZIhvcNAQELBQADgYEAuIC/
svWDlVGBan5BhynXw8nGm2DkZaEElx0bO+kn+kPWiWo8nr8o0XU3IfMNZBeyoy2D
Uv9X8EKpSKrYhOoNgAVxCqojtGzG1n8TSvSCueKBrkaMWfvDjG1b8zLshvBu2ip4
q/I2+0j6dAkOGcK/68z7qQXByeGri3n28a1Kn6o=
-----END CERTIFICATE-----
"""

# add encrypted remote syslog configuration to the appliance
# guardium_cli.add_remote_syslog(
#     params={
#             'encryption': 'encrypted',  # [str][required] 'encrypted' | 'non_encrypted'
#             'facility': 'daemon',  # [str][required] syslog source and topic
#             'priority': 'all',  # [str][required] syslog message priority (urgency)
#             'host': 'raptor.gdemo.com',  # [str][required] -- hostname or IP address
#             'port': '514',  # [str][optional] -- default 514
#             'protocol': 'tcp',  # [str][required]  -- 'udp' or 'tcp'
#             'format': 'default',  # [str][optional]  message format default is syslog
#             'escape_control_characters': 'off',  # [str][optional] escape control characters
#             'max_message_size': '6',  # [optional][5k] | '2' [10k]| '3' [15k] | '4' [20k]| '5' [23k] | '6' [64k],
#             'public_cert_pem': public_ca_pem,  # [str] Public CA certificate (.pem) from the rsyslog receiver
#             'test_msg': False  # Uses 'show remotelog test' to send a test message and observe it leave in tcpdump
#         },
#     clear_existing=False)  # clears existing entry for the host + facility.priority if it exists

# add unencrypted remote syslog configuration to the appliance
guardium_cli.add_remote_syslog(
    params={
            'encryption': 'non_encrypted',  # [str][required] 'encrypted' | 'non_encrypted'
            'facility': 'user',  # [str][required] syslog source and topic
            'priority': 'all',  # [str][required] syslog message priority (urgency)
            'host': 'raptor.gdemo.com',  # [str][required] -- hostname or IP address
            'port': '514',  # [str][optional] -- default 514
            'protocol': 'tcp',  # [str][required]  -- 'udp' or 'tcp'
            'format': 'default',  # [str][optional]  message format default is syslog
            'escape_control_characters': 'off',  # [str][optional] escape control characters
            'max_message_size': None,  # [optional][5k] | '2' [10k]| '3' [15k] | '4' [20k]| '5' [23k] | '6' [64k],
            'public_cert_pem': None,  # [str] Public CA certificate (.pem) from the rsyslog receiver
            'test_msg': True  # Uses 'show remotelog test' to send a test message and observe it leave in tcpdump
        },
    clear_existing=True)  # clears existing entry for the host + facility.priority if it exists

