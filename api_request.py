import configparser
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_token(client_id, client_secret, partner_url='https://sandbox-partners-api.airalo.com/v2/token'):
   
    multipart_data = MultipartEncoder(
        fields={
            'grant_type': 'client_credentials'
        }
    )

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Host': 'partner.airalo.com'  # Ensure this matches the actual host
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(
        partner_url,
        data=payload,
        headers=headers
    )
   
    # Check if the token request was successful
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['data']['access_token']
        print(f"\033[92m--------Authentication Success----------------\033[0m")
        return access_token
    else:
        raise Exception("\033[91m----Authentication Error-------\033[0m")
        
def read_expected_json(file_name=None):
    file_name = file_name + ".json"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def send_api_request(endpoint_url, method="GET", headers=None, data=None, params=None):
    """
    Sends an HTTP request and returns the response.

    Args:
    - url (str): The endpoint URL.
    - method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
    - headers (dict): Optional HTTP headers.
    - data (dict): Optional data for POST/PUT requests.
    - params (dict): Optional query parameters for GET requests.

    Returns:
    - response: The HTTP response.
    """
    response = requests.request(method, endpoint_url, headers=headers, data=data, params=params)
    return response


def verify_response(response, test_case, expected_status_code, expected_json=None):
    """
    Verifies that the HTTP response matches the expected values.

    Args:
    - response: The HTTP response to verify.
    - expected_status_code (int): The expected status code.
    - expected_json (dict): Optional, the expected JSON response.

    Raises:
    - AssertionError if the verification fails.
    """
    assert response.status_code == expected_status_code, f"Expected {expected_status_code}, got {response.status_code}"
    
    if test_case == 1:
        resp = response.json()
        if 'package_id' in resp['data'].keys():
            assert resp['data']['package_id'] == expected_json['data']['package_id'], f"Assertion failed for Package: Expected {expected_json['data']['package_id']}, got {resp['data']['package_id']}"
            assert resp['data']['quantity'] == expected_json['data']['quantity'], f"Assertion failed for Package: Expected {expected_json['data']['quantity']}, got {resp['data']['quantity']}"
            print ("\033[92m--------Endpoint 1 test execution successful----------------\033[0m")
    if test_case == 2:
        response_iccid = list()
        response_iccid = sorted([i['iccid'] for i in response.json()['data']])
        expected_iccid = sorted([i['iccid'] for i in expected_json.json()['data']['sims']])
        for i in range(0, len(expected_iccid)):
            assert response_iccid[i] == expected_iccid[i]
        print ("\033[92m--------Endpoint 2 test execution successful----------------\033[0m")
            



def read_config(config=None):
    """
    This method will read the configs required from a config file in parent directory if path is not provided
    """
    try:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"\033[91The config file does not exist in the path : '{config_file}'\033[0m")           
        config.read(config_file)      

    except:
        raise Exception("\033[91mUnexpected error occurred while reading config file\033[0m")


def api_test(endpoint_url, method, headers, data, params):
    """
    Test an API endpoint by sending a request and verifying the response.

    This test function will be executed multiple times with different inputs, 
    thanks to pytest's parametrize feature.

    Args:
    - endpoint_url (str): The endpoint URL.
    - method (str): The HTTP method.
    - headers (dict): Optional HTTP headers.
    - data (dict): Optional data for POST/PUT requests.
    - params (dict): Optional query parameters for GET requests.
 
    Raises:
    - AssertionError if the verification fails.
    """
    response = send_api_request(endpoint_url, method, headers, data, params)
    return response


if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    
    read_config(config)
    

    client_id = config.get('SANDBOX', 'client_id')
    client_secret = config.get('SANDBOX', 'client_secret')
    partner_url = config.get('SANDBOX', 'partner_url')
    endpoint1_url = config.get('SANDBOX', 'endpoint1_url')
    endpoint2_url = config.get('SANDBOX', 'endpoint2_url')

    access_token = get_token(client_id, client_secret)

    api_headers = {'Authorization': f'Bearer {access_token}'}
    ep1_payload = {
        'quantity' : 6,
        'package_id' : 'merhaba-7days-1gb'  
    }

    ep1_expected_json = read_expected_json("endpoint1")

    data = {
        'grant_type': 'client_credentials'
    }
    
    """ 
    Endpoint 1:
        ○ Use this endpoint to POST an order for 6 &quot;merhaba-7days-1gb&quot; eSIMs.
        ○ Ensure you have a valid OAuth2 token before making the request.  
    """

    endpoint1_resp = api_test(endpoint_url=endpoint1_url, method='POST', headers=api_headers, data=None, params=ep1_payload)
    verify_response(endpoint1_resp, 1, 200, ep1_expected_json)    
    """
    Endpoint 2:
        ○ Use this endpoint to GET a list of eSIMs.
        ○ Ensure the list contains 6 eSIMs, and that all of them have the merhaba-7days-1gb; package slug.
        ○ Ensure you have a valid OAuth2 token before making the request.
    """
    endpoint_resp = api_test(endpoint_url=endpoint2_url, method='GET', headers=api_headers, data=data, params={'limit' : 6})
    verify_response(endpoint_resp, 2, 200, endpoint1_resp)   



