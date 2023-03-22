# endpoint_isolation

This is a test file to show the abilities of isolating a Secure Endpoint connector using the API.

To set up, create your Secure Endpoint API credentials and insert them into the script.  It isn't ideal to have these in the file itself but is fine for a simple test.  If you plan to use this in some type of production environment, remove the credentials from the script and add them to an environment variable instead.  Finally, add the hostname of the endpoint you would like to isolate for the test.

The test will use the API to pull the connector GUID using the hostname, isolate the endpoint using the API and the connector GUID, wait 60 seconds to ensure the connector has been isolated, pull the trajectory information for the connector using the API and and the connector GUID, and remove the endpoint from isolation using the API and the connector GUID.
