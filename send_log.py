from pathlib import Path
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from bs4 import BeautifulSoup
from tabulate import tabulate
import requests
import certifi

def upload_to_uesp(username, lua_file_path):
    # Prepare the payload
    payload = {
        'wikiUserName': username,
        'MAX_FILE_SIZE': '120000000'
    }

    upload_url = 'https://esolog.uesp.net/submit.php'

    fields = {
        'logfile': ('uespLog.lua', open(lua_file_path, 'rb'), 'application/octet-stream')
    }

    path = Path(lua_file_path)
    total_size = path.stat().st_size
    filename = path.name

    # Submit the data with SSL certificate verification
    with tqdm(
        desc=filename,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        with open(lua_file_path, "rb") as f:
            fields["logfile"] = (filename, f)
            e = MultipartEncoder(fields=fields)
            m = MultipartEncoderMonitor(
                e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
            )
            headers = {"Content-Type": m.content_type}
            response = requests.post(upload_url, data=m, headers=headers, verify=certifi.where())

    # Handle the response
    if response.status_code == 200:

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
lua_file_path = r"C:\Users\johan\OneDrive\Documents\Elder Scrolls Online\live\SavedVariables\uespLog.lua.old"

upload_to_uesp(username, lua_file_path)
