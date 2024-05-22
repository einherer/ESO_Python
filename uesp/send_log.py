from pathlib import Path
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from bs4 import BeautifulSoup
from tabulate import tabulate
import requests
import certifi
import argparse

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
            fields = {'logfile': (filename, f, 'application/octet-stream')}
            e = MultipartEncoder(fields=fields)
            m = MultipartEncoderMonitor(
                e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
            )
            headers = {"Content-Type": m.content_type}
            response = requests.post(upload_url, data=m, headers=headers, verify=certifi.where())

    # Handle the response
    if response.status_code == 200:
        print(beautify_response(response.text))
    else:
        print(f"Upload failed with status code {response.status_code}")
        print(response.text)  # Print any error message returned by the server


def beautify_response(response: str) -> str:
    soup = BeautifulSoup(response, 'html.parser')
    # Find the table element and get its contents
    table = soup.find('table', {'id': 'maintable'})
    
    # Extract the text and add appropriate formatting
    result = table.find_all('td')[1].get_text(separator='\n')
    lines = result.strip().split('\n')
    
    # Clean up the formatting
    formatted_lines = []
    for line in lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            formatted_lines.append(f'{key}:'.ljust(25)+f'{value}')
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)



# Example usage
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="use with caution")
    parser.add_argument('option', type=str, nargs='?', default='upload', help="'upload' - uploading a log \n'beautify' - test the responseparser")
    
    args = parser.parse_args()
    
    if args.option == "beautify":
        with open("./example_response.html", 'rb') as file:
            print(beautify_response(file.read()))
    else:
        username = "Einherer"
        lua_file_path = r"C:\Users\johan\OneDrive\Documents\Elder Scrolls Online\live\SavedVariables\uespLog.lua"
        upload_to_uesp(username, lua_file_path)