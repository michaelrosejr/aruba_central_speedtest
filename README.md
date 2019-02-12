# Aruba Central Speed Test Scheduler



## Getting Started
To start, please login to Aruba Central and create an API System Token Under Maintenance -> API Gateway. Once done, download the token and save it as ``defualt.token.json`` in the directory where you installed this script.

You'll also need to create a ``config.yml`` file. There's a ``sample.config.yml`` that you should use as a template. You'll need the following info:

URL for access the Aruba Central API for your region
customer_id for identify who you are as a customer
client_id for identify your API ID
client_secret for accessing your API

once done, run ``do_speed_test.py iPerf_Server  AP_SerialNumber`` and it will refresh your Aruba Central token and post the access_token and refresh_token on the scren.

## Start-Up
Onces the ``default.token.json`` and ``config.yml`` files have been created. 

For those that don't want to install the Python modules used by this script, you can run the following command:

```
pipenv run do_speed_test.py iperf_server Serial_Numbrer
```

You can also run it by entering the pipenv shell:

```
pipenv shell
do_speed_test.py iperf_server Serial_Numbrer
```

if you plan to run it frequently, then install the necessary python modules and install the ``do_speed_test.py iperf_server Serial_Numbrer`` as a python module.


## Additional Features
If you have more than one API account that you can to refresh token for, you can set them up in the config file as follows:

```
SecondApi:
   url: https://apigw-prod2.central.arubanetworks.com
   envapi:  prod
   customer_id: 1234567...
   client_id: 34567...
   client_secret: 9876543...

```

## Authors

* **Michael Rose Jr.** - [GitHub](https://github.com/michaelrosejr)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


