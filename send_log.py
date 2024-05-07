import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import certifi

def upload_to_uesp(username, lua_file_path):
    # Prepare the payload
    payload = {
        'wikiUserName': username,
        'MAX_FILE_SIZE': '120000000'
    }

    files = {
        'logfile': ('uespLog.lua', open(lua_file_path, 'rb'), 'application/octet-stream')
    }

    # Path to the CA certificate bundle
    ca_bundle_path = certifi.where()

    # Submit the data with SSL certificate verification
    response = requests.post('https://esolog.uesp.net/submit.php', data=payload, files=files, verify=ca_bundle_path)
####### TODO: beautify resprone #####################################
    # Handle the response
    if response.status_code == 200:
        # Parse the HTML response
        # with open("example_response.html", 'w') as html_file:
        #      html_file.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table element and print its contents
        table = soup.find('table', {'id': 'maintable'})
        # Parse the response data
        response_data = table.get_text().split('\n')
        
        # Format the response data into a table
        formatted_data = []
        for line in response_data:
            if line.strip():  # Ignore empty lines
                parts = line.split(':')
                formatted_data.append([parts[0].strip(), ':'.join(parts[1:]).strip()])

        # Print the formatted data as a table
        print(tabulate(formatted_data, headers=["Attribute", "Value"]))
    else:
        print(f"Upload failed with status code {response.status_code}")
        print(response.text)  # Print any error message returned by the server

# Example usage
username = "Einherer"
lua_file_path = r"C:\Users\johan\OneDrive\Documents\Elder Scrolls Online\live\SavedVariables\uespLog.lua"

upload_to_uesp(username, lua_file_path)
