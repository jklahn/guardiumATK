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


# example of adding an unencrypted remote syslog configuration to the appliance
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
            'send_test_msg': True  # Uses 'show remotelog test' to send a test message and observe it leaving in tcpdump
        },
    clear_existing=True)  # clears existing entry for the host + facility.priority if it exists

# For encrypted TCP, you need a CA cert; Don't store this in your code. This is only for example purposes.
public_ca_pem = """
-----BEGIN CERTIFICATE-----
MIIFpzCCA4+gAwIBAgIUHEMY4JcZ8zAtvPVCPm57Mep2GdwwDQYJKoZIhvcNAQEL
BQAwYzELMAkGA1UEBhMCWFgxEDAOBgNVBAgMB0dlb3JnaWExEDAOBgNVBAcMB0F0
bGFudGExDDAKBgNVBAoMA0lCTTEPMA0GA1UECwwGRGF0YUFJMREwDwYDVQQDDAhH
dWFyZGl1bTAeFw0yNTA2MTMxNDI3MDJaFw0zNTA2MTExNDI3MDJaMGMxCzAJBgNV
BAYTAlhYMRAwDgYDVQQIDAdHZW9yZ2lhMRAwDgYDVQQHDAdBdGxhbnRhMQwwCgYD
VQQKDANJQk0xDzANBgNVBAsMBkRhdGFBSTERMA8GA1UEAwwIR3VhcmRpdW0wggIi
MA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDBFXbRNdkepyv8YGJvG9INaQA5
OE5c9xJqn7t2xo3lSWZpudLyKnl/6/XksDUVdyipsR5owVml36itVGpi0F2XZCjb
br5ysmBMHEIzt0M/Yarwqo1n2d4bWLB7fsdDGxZOCaAfKsoMIlKtJLmA6AxZte8a
cc8OmKGnC5Jg0S4jzkzJ85cZqFwpR9ouJfbhBNIgICw7ZsJBcFi/ipXBBqOZbQrF
ZfrzLxUHj1kokT6MiofN7GXP3mY+MOwEc/Ra8rOpnG6o5V24t5TQM65XW25YqT+U
qBCCTQoSZ3xZlD5Dt7Lkfngjf1xzC161ycQRyS47zbpfqkebn8ggEjOQ81OXLKJ6
H2GQVA6FTUxDEya8dLPfVRBQjt2Pbjd1KH3elWVC3dg1nuIjhNvsj+yQ5jjjtGRE
ndlNoaV+M8dAUikVwZmG1Wbolmv7Zzt7TdMYVYLevJXm/BHVZwh/e4sJevfG8Uw6
ppploQLS3N7x2Ic/EsglYqXBPqoHUpQpX/KvRJ9ftf0vjOnzVECHjtpHTcdppFZm
I4Pb4mpasyRtGsDAayB0Aqf73fSG0n1k7m4aIZ5vm2EUZilwwuPQ/qdRljTQnYPD
t1dB3Nb3xXiWTjSs74WzFpMqBdQLVpiWHGA7+zHZq6Ipgoc61e4TuSCd3QfA2Lnk
07jslIAqZ/bFVJWRyQIDAQABo1MwUTAdBgNVHQ4EFgQUTh/slv9yQksnlYXe7gjI
qr2FMrEwHwYDVR0jBBgwFoAUTh/slv9yQksnlYXe7gjIqr2FMrEwDwYDVR0TAQH/
BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAgEAfbxrYc51569SLkYFufVXV+mK4TSO
FAtYYaEc1PdrEKGMa6yBbBk0sL4ZT6+DyaWvscOBFKVtG9J0YMBsjKaxirTTw4MA
hYw7HrMDPujebAulIQBCyTWRsSDf47UzvjU3J73YN8EeFRA8pZNhEeyn/1SzVkj2
HlXHaAvjDTRVSbuweYjVT6Wwnp4vxZy6ynS7lpgT+FbBv9aKrw0fer5bYpJpi1i2
x7Ym4Pd32WgdQ4hKFlKIAlHF5mBvBQIJ4mdhzqZWPMBc32nUEJt70xoymxHo9yQ1
tsTOchYvdbXbO7X0O3DA5Lxmzr7AB3vifkkmvndk5EV8pFxL7WnsyU/TI8YvDcFO
nwV5pkH4wN/9h3TnVFM8TjhB1xLwAdXqADjcKCTyFLsJavZlMdpwYMJ3yoXC3j5b
bNyx9/eWXm3SkCHQlJksB4zngWUg4RR+gDcb9p3zxhFSx1lebgQpir9YmpBjaoNi
1pvpHTUyKXLVo2Cn0OC9V+S6GPnOBqAK9E69WpmPVW7I1YvfERXOCoXvJz3BFFSE
3mfqyYqXiovYFp6dFochppgoCLJi5Uurzic/+SFFEms7+ldBFENgCpdMpIqUgrx+
CfU4UN7/IUJMZ9cxgn3DKuEYEhnMyawis06TiiDNtfBv6cnJQmuEuqNd1tr/JqoF
G0M9BmBN3pFiLnI=
-----END CERTIFICATE-----
"""

# Example of adding an encrypted remote syslog configuration to the appliance (uncomment to use)
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
#             'send_test_msg': True  # Uses 'show remotelog test' to send a test message and observe it leaving in tcpdump
#         },
#     clear_existing=True)  # clears existing entry for the host + facility.priority if it exists
