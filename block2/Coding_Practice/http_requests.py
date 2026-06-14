import requests

def fetch_example_website():
    # 1. Define the target URL
    url = 'http://example.com'
    
    # 2. Create a dictionary for custom headers
    # This overrides the default 'python-requests/x.x' user-agent
    custom_headers = {
        'User-Agent': 'MyPythonStudentClient/1.0'
    }

    try:
        # 3. Perform the GET request, passing in the custom headers
        print(f"Attempting to connect to {url}...")
        response = requests.get(url, headers=custom_headers)
        
        # raise_for_status() will throw an exception if the server 
        # returned an error code (like 404 or 500)
        response.raise_for_status()

        # 4. Extract and print the requested information
        print("\n=== HTTP Status Code ===")
        print(response.status_code)

        print("\n=== Response Headers ===")
        # response.headers behaves like a dictionary
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        print("\n=== Response Body ===")
        # response.text contains the decoded string of the body (HTML)
        print(response.text)

    # 5. Exception handling for network errors
    except requests.exceptions.RequestException as e:
        # RequestException is the base class for all exceptions in the requests module
        print(f"\n[Error] A network or HTTP error occurred: {e}")

if __name__ == '__main__':
    fetch_example_website()
    x = input()