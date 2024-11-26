import requests

# URL of the raw CSV file
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    with open("raw_data/owid-co2-data.csv", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully!")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
