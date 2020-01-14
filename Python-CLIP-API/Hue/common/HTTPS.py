import requests

GET = 0; PUT = 1; POST = 2; DELETE = 3;
defaultTimeout = 10
defaultVerify = False

def request(rtype, address, api, **kwargs):
    '''
    Send HTTPS request method to address.

    Parameters:
    rtype: Method type: GET, PUT, POST, DELETE.
    address: Request address.
    api: API address.
    (optional) params: Paramaters for request.
    (optional) verify: Verify certificate.
    (optional) timeout: Maksimum time to wait for reply.

    Returns:
    string or None: API key from bridge, or None on fault.
    '''
    response = None
    kwargs = {
        "rtype": rtype,
        "address": "https://" + address + api,
        "params": kwargs.get('params', {}),
        "verify": kwargs.get('verify', defaultVerify),
        "timeout": kwargs.get('timeout', defaultTimeout)
    } # Create paramater dictionary, which can be passed to the specific request function
    print("Sending request type {} to address {}, with data {}".format(rtype, address, kwargs.get('params', {})))
    response = __sendRequest(**kwargs)
    response_code = __getResponseCode(response) # Get response code
    data = __getData(response) # Get data
    print("Request returned response {} and data {}".format(response_code,data))
    return response_code, data # Return response and data

def __sendRequest(**kwargs): # Determine request type
    rtype = kwargs.get("rtype", None)
    switcher = {
        0: __getRequest,
        1: __putRequest,
        2: __postRequest,
        3: __deleteRequest
    }
    function = switcher.get(rtype, lambda: "Exception on __requestType(), invalid function call")
    return function(**kwargs)

def __getRequest(**kwargs):
    response = None
    try: 
        response = requests.get(
            kwargs.get('address', "1.1.1.1"), 
            verify = kwargs.get('verify', defaultVerify),
            timeout = kwargs.get('timeout', defaultTimeout)
        )
    except:
        print("Exception on __getRequest(): Unable to send request.")
    return response

def __putRequest(**kwargs):
    response = None
    try: 
        response = requests.put(
            kwargs.get('address', "1.1.1.1"),
            json = kwargs.get('params', {}), 
            verify = kwargs.get('verify', defaultVerify),
            timeout = kwargs.get('timeout', defaultTimeout)
        )
    except:
        print("Exception on __putRequest(): Unable to send request.")
    return response

def __postRequest(**kwargs):
    response = None
    try: 
        response = requests.post(
            kwargs.get('address', "1.1.1.1"),
            json = kwargs.get('params', {}), 
            verify = kwargs.get('verify', defaultVerify),
            timeout = kwargs.get('timeout', defaultTimeout)
        )
    except:
        print("Exception on __postRequest(): Unable to send request.")
    return response

def __deleteRequest(**kwargs):
    response = None
    try: 
        response = requests.delete(
            kwargs.get('address', "1.1.1.1"),
            json = kwargs.get('params', {}), 
            verify = kwargs.get('verify', defaultVerify),
            timeout = kwargs.get('timeout', defaultTimeout)
        )
    except:
        print("Exception on __deleteRequest(): Unable to send request.")
    return response

def __getResponseCode(response): # Get response code form requests, or None on fault
    code = None
    try:
        code = response.status_code
    except:
        print("Exception on __getResponseCode(): No status code returned.")
    return code

def __getData(response): # Check for data in response
    data = None
    try:
        data = response.json()
    except:
        print("Exception on __getData(): No data returned.")
    return data