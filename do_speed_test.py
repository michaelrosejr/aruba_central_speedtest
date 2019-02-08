#!/usr/bin/env python3
import requests
import json
import json
import yaml
import logging
import time
import os
import sys

from central import auth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# serial = "CM0300585"
# iperf_server = "62.210.18.40"

account = "default"
baseurl = "https://apigw-prod2.central.arubanetworks.com"

try:
    serial = str(sys.argv[2])
except:
    print("Serial  missing: app.py iperf_server serial_number")

try:
    iperf_server = str(sys.argv[1])
except:
    print("Serial  missing: app.py iperf_server serial_number")

logging.info("Account set to: %s", str(account))

print("SERIAL: ", serial)

def set_speed_test(sessiondata, serial, iperf_server):
    access_token = sessiondata['access_token']
    url = baseurl + "/device_management/v1/device/" + serial + "/action/speedtest"
    params = {"access_token": access_token}
    post_data = {'host': iperf_server, 'options': 'tcp'}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    speed_qry = requests.post(url, headers=headers,
                              data=json.dumps(post_data), params=params)
    return(speed_qry.text)


def start_ts(sessiondata, serial, squeued):
    url = baseurl + "/troubleshooting/v1/devices/" + serial
    params = {"access_token": sessiondata['access_token']}
    post_data = {
                    "device_type": "IAP",
                    "commands": [
                        {
                        "command_id": 167,
                        "arguments": [
                            {
                            "name": "string",
                            "value": "string"
                            }
                        ]
                        }
                    ]
                }
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    print(json.dumps(post_data))
    speed_start = requests.post(url, headers=headers,
                              data=json.dumps(post_data), params=params)
    return(speed_start.text)

def get_speed_test(sessiondata, serial, session_id):
    url = baseurl + "/troubleshooting/v1/devices/" + serial
    print("GETSPEED: ", url)
    data = "{}"
    params = {"access_token": sessiondata['access_token'], "session_id": session_id}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    print("GETSPEED: ", url, params, headers)
    speed_results = requests.get(url, headers=headers, params=params)
    return(speed_results.text)

def get_status(sessiondata, task_id):
    url = baseurl + "/device_management/v1/status/" + str("task_id")
    params = {"access_token": sessiondata['access_token']}

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    task_results = requests.get(url, headers=headers, params=params)
    return(task_results.text)

def read_config():
    if os.path.isfile("config.yml"):
        with open("config.yml", 'r') as ymlfile:
            data = yaml.load(ymlfile)
        return data
    else:
        print("Please read the README file and create the config.yml file using the sample.config.yml as a guide")


def get_networks(config, sessiondata, tokenfile, account):
    service_url = config[account]['url'] + "/monitoring/v1/networks"
    params = {'access_token': sessiondata['access_token']}
    headers = {"Accept": "application/json"}

    r = requests.get(service_url, params=params, headers=headers)
    if r.status_code == 401:
        # print(vars(get_access_token))
        # print('Status:', r.status_code, 'Headers:', r.headers,
        #       'Error Response:', r.reason)
        return_error = json.loads(r.text)
        logging.warning(r.text)
        if return_error["error"] == "invalid_token":
            logging.warning("Invalid or expired token. Refreshing...")
            newsession = auth.CentralAuth.refresh_token(
                config, sessiondata, tokenfile, account)
            newparams = {'access_token': newsession['access_token']}
            r = requests.get(service_url, params=newparams, headers=headers)
    # return(r.json())
    return(r.status_code)


def main():
    # try:
        config = read_config()
        filetoken = account + "." + config["tokenfile"]
        logging.info("Token file: %s", filetoken)
        if os.path.isfile(filetoken):
            with open(filetoken) as exjsonfile:
                sessiondata = json.load(exjsonfile)
                logging.info("Querying Central...")
        else:
            print("Please login to Aruba Central and download the token file and save it as " +
                  account + ".token.json ")
        d = get_networks(config, sessiondata, filetoken, account)
        if d == 200:

            squeued = set_speed_test(sessiondata, serial, iperf_server)
            print("squeued: ")
            
            print("Checking Status...task id: ", json.loads(squeued)['task_id'])
            task_id = json.loads(squeued)['task_id']
            stat_check = get_status(sessiondata, task_id)
            print("TEST")
            print(stat_check)
            started = json.loads(start_ts(sessiondata, serial, squeued))
            print("Sending speed test to device(s)")
            time.sleep(5)
            print(started)
            print("SESSION ID: ", started['session_id'])
            print("Waiting 20 seconds for test to run...")
            time.sleep(20)
            speed_details = json.loads(get_speed_test(sessiondata, serial, started['session_id']))
            print(speed_details["message"])
            print(speed_details["output"])

    # except:
    #     print("Something broke when using: " + account +
    #           ". I don't know what. This is a catch-all error.")


if __name__ == "__main__":
    logging.info("Executing main...")
    main()


# speed_output = '{ "hostname": "04BD88C14C26:661:4414", "message": "Successfully completed troubleshooting session 13 of device CM0300585", "output": "\n=== Troubleshooting session started. === \n\n\n===================================\nOutput Time: 2019-02-06 04:27:15 UTC\n\n\nCOMMAND=show speed-test data\n\r\nSpeed Test results : \nSpeed Test Error :Test data not available\n\n=== Troubleshooting session completed. ===\n", "serial": "CM0300585", "status": "COMPLETED" }'

# print(speed_output)


