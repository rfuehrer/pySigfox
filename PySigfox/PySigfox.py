#!/usr/bin/python

import os
import sys
import json
import requests
from pprint import pprint

class PySigfox:
    def __init__(self, login, password):
        if not login or not password:
            print("Please define login and password when initiating PySigfox class!")
            sys.exit(1)
        self.login    = login
        self.password = password
        self.api_url  = 'https://backend.sigfox.com/api/'

    def login_test(self):
        """Try to login into the  Sigfox backend API - if unauthorized or any other issue raise Exception

        """
        url = self.api_url + 'devicetypes'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        if r.status_code != 200:
            raise Exception("Unable to login to Sigfox API: " + str(r.status_code))

    def device_types_list(self):
        """Return list of device types IDs

        """
        out = []
        url = self.api_url + 'devicetypes'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        for device in json.loads(r.text)['data']:
            out.append(device['id'])
        return out

    def device_list(self, device_type_id = 0):
        """Return array of dictionaries - one array item per device.

        If device_type_id is not set devices of all device types are returned!
        """
        device_type_ids = []
        out = []
        if device_type_id != 0:
            device_type_ids.append(device_type_id)
        else:
            device_type_ids = self.device_types_list()

        for device_type_id in device_type_ids:
            # print("Getting data for device type id " + device_type_id)
            url = self.api_url + 'devicetypes/' + device_type_id + '/devices'
            r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
            out.extend(json.loads(r.text)['data'])
        return out

    def device_messages(self, device_id):
        """Return array of messages from device with ID defined in device_id.

        """
        url = self.api_url + 'devices/' + device_id + '/messages'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        return json.loads(r.text)['data']
