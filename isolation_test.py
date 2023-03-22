import json
import requests
import time

# Enter your client ID and API key from Secure Endpoints
# https://console.amp.cisco.com/api_credentials
# Since the computers and isolation API calls are V1, you only need to use Secure Endpoints API credentials.
# If you decide to use a V3 API call later, you'll need to add SecureX API Credentials
# https://developer.cisco.com/docs/secure-endpoint/#!authentication
# Best to store these in an environment variable but putting here for simplicity in the example
CLIENT_ID = "abcdef0123456789abcd"
API_KEY = "abcdef01-abcd-1234-5678-abcdef012345"

# You would need to provide your hostname programmatically here.
HOSTNAME = "DESKTOP-ABCDEFGH"

# API documentation
# https://developer.cisco.com/docs/secure-endpoint/
base_url = "https://api.amp.cisco.com/v1"
auth = (CLIENT_ID, API_KEY)

def get_connector_guid():
    # Specify the computers URL to pull the computers information (guid is required for the isolation call)
    # https://developer.cisco.com/docs/secure-endpoint/#!v1-api-reference-computer
    computers_url = f"{base_url}/computers"
    data = {"hostname": HOSTNAME}

    # Make the request
    comp_response = requests.get(computers_url, auth=auth, data=data)
    # Convert resposne to JSON
    comp_response_json = json.loads(comp_response.content)
    # Extract the connector GUID
    connector_guid = comp_response_json['data'][0]['connector_guid']
    return connector_guid

def isolate_endpoint(connector_guid):
    # https://developer.cisco.com/docs/secure-endpoint/#!endpoint-isolation
    isolation_url = f"{base_url}/computers/{connector_guid}/isolation"

    # Isolate the endpoint
    isolate_response = requests.put(isolation_url, auth=auth)

    if isolate_response.status_code == 200:
        # Convert response to JSON
        isolate_response_json = json.loads(isolate_response.content)
        unlock_code = isolate_response_json['data']['unlock_code']
        print("Endpoint successfully isolated")
        return unlock_code
    elif isolate_response.status_code == 409:
        print("Endpoint is already isolated")
        return ""
    else:
        print("Error isolating endpoint")
        return ""

def remove_isolation(connector_guid, unlock_code):
    # https://developer.cisco.com/docs/secure-endpoint/#!endpoint-isolation
    isolation_url = f"{base_url}/computers/{connector_guid}/isolation"

    # Remove the isolation
    remove_isolation_response = requests.delete(isolation_url, auth=auth, data={"unlock_code": unlock_code})
    if remove_isolation_response.status_code == 200:
        # Convert response to JSON
        remove_isolation_response_json = json.loads(remove_isolation_response.content)
        print("Endpoint is no longer isolated")
    elif remove_isolation_response.status_code == 409:
        print("Endpoint is not isolated")
    else:
        print("Error removing isolation from endpoint")

def get_connector_trajectory(connector_guid):
    traj_url = f"{base_url}/computers/{connector_guid}/user_trajectory"
    traj_response = requests.get(traj_url, auth=auth, data={"hostname": HOSTNAME})
    print(json.loads(traj_response.content))

def run_connector_test():  
    print("[+] Running connector test")
    print("[+] Pulling connector GUID using hostname")
    connector_guid = get_connector_guid()
    print("[+] Isolating endpoint")
    unlock_code = isolate_endpoint(connector_guid)
    print("[+] Getting connector trajectory")
    get_connector_trajectory(connector_guid)
    print("[+] Waiting 60 seconds before removing isolation")
    time.sleep(60)  
    print("[+] Removing endpoint from isolation")
    remove_isolation(connector_guid, unlock_code)

    # You can also check the isolation status of an endpoint
    # status_url = f"{base_url}/computers/{connector_guid}/isolation"
    # status_response = requests.get(status_url, auth=auth)
