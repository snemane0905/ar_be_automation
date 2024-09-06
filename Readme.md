
# API Testing Automation

This project is designed to test API endpoints using Python. It includes functionality for OAuth2 authentication, sending API requests, verifying responses, and comparing actual vs expected results.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints Tested](#api-endpoints-tested)
- [Code Structure](#code-structure)

---

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/snemane0905/ar_be_automation.git
   ```
2. **Navigate into the project directory:**

    ```bash
    cd ar_be_automation
    ```
3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```
### Dependencies:

- `requests`
- `requests_toolbelt`
- `configparser`

## Configuration

Before running the tests, you need to configure the API credentials and endpoint URLs. This is done via the `config.ini` file in the root directory.

### `config.ini` Format:

```ini
[SANDBOX]
client_id = your_client_id
client_secret = your_client_secret
partner_url = https://sandbox-partners-api.airalo.com/v2/token
endpoint1_url = https://api.example.com/endpoint1
endpoint2_url = https://api.example.com/endpoint2
```

Make sure to update the values with your actual client credentials and endpoint URLs.

## Usage

### Run the tests:

1. **Once you have configured the `config.ini` file, you can run the main script:**

```bash
python api_request.py
```

2. **Check the output:**

The test results will be printed in the console, including whether the authentication was successful and whether each endpoint's execution was successful.

## API Endpoints Tested

1. **Endpoint 1:**
   - Sends a `POST` request to place an order for 6 "merhaba-7days-1gb" eSIMs.
   - Verifies that the `package_id` and `quantity` match the expected values.

2. **Endpoint 2:**
   - Sends a `GET` request to retrieve a list of eSIMs.
   - Verifies that the list contains 6 eSIMs and checks for the correct `package_slug`.


## Code Structure

- `get_token()`: Retrieves an OAuth2 token using the client credentials.
- `read_config()`: Reads the configuration from `config.ini`.
- `read_expected_json(file_name)`: Reads the expected JSON response from a file.
- `api_test()`: Executes the API test with provided parameters.
- `send_api_request(endpoint_url, method, ...)`: Sends an HTTP request to the specified API endpoint.
- `verify_response(response, test_case, ...)`: Compares the actual API response with the expected values.


### Example Flow:

1. **Get OAuth2 Token**: The token is fetched using client credentials.
2. **Test Endpoint 1**: Sends a `POST` request to place an order for 6 eSIMs.
3. **Test Endpoint 2**: Sends a `GET` request to retrieve the list of eSIMs.


