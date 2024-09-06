import configparser
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


def verify_response(response, expected_status_code, expected_json=None):
    """
    Verifies that the HTTP response matches the expected values.

    Args:
    - response: The HTTP response to verify.
    - expected_status_code (int): The expected status code.
    - expected_json (dict): Optional, the expected JSON response.

    Raises:
    - AssertionError if the verification fails.
    """
    import ipdb;ipdb.set_trace()
    assert response.status_code == expected_status_code, f"Expected {expected_status_code}, got {response.status_code}"
    
    if expected_json:
        assert response.json() == expected_json, f"Expected JSON {expected_json}, got {response.json()}"



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


def api_test(endpoint_url, method, headers, data, params, expected_status_code, expected_json):
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
    - expected_status_code (int): The expected HTTP status code.
    - expected_json (dict): The expected JSON response.

    Raises:
    - AssertionError if the verification fails.
    """
    import ipdb;ipdb.set_trace()
    response = send_api_request(endpoint_url, method, headers, data, params)
    verify_response(response, expected_status_code, expected_json)


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

    ep1_expected_json = {

    }

    ep2_expected_json = {}
    data = {
        'grant_type': 'client_credentials'
    }
    
    """ 
    Endpoint 1:
        ○ Use this endpoint to POST an order for 6 &quot;merhaba-7days-1gb&quot; eSIMs.
        ○ Ensure you have a valid OAuth2 token before making the request.  
    """

    # response = requests.post(endpoint1_url, json=ep1_payload, headers=headers)

    api_test(endpoint_url=endpoint1_url, method='POST', headers=api_headers, data=None, params=None, expected_status_code=200, expected_json=ep1_expected_json)
    
    """
    Endpoint 2:
        ○ Use this endpoint to GET a list of eSIMs.
        ○ Ensure the list contains 6 eSIMs, and that all of them have the merhaba-7days-1gb; package slug.
        ○ Ensure you have a valid OAuth2 token before making the request.
    """
    api_test(endpoint_url=endpoint2_url, method='GET', headers=api_headers, data=data, params={'limit' : 6}, expected_status_code=200, expected_json=ep2_expected_json)




