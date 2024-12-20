import requests
import json


# Step 1: Create sea with name and description
url_create_sea = "http://localhost:8000/sea/"
headers = {"Content-Type": "application/json"}
data_create_sea = {"name": "Test1", "description": "Test1 description"}

response_create_sea = requests.post(
    url_create_sea, headers=headers, data=json.dumps(data_create_sea)
)

# Get the id from the response
if response_create_sea.status_code == 200:
    sea_id = response_create_sea.json().get("id")
    print(f"Sea ID: {sea_id}")
else:
    print(f"Failed to create sea: {response_create_sea.status_code}")
    exit(1)

# Step 2: Call the sea API using the sea ID
url_sea_status = f"http://localhost:8000/sea/{sea_id}"
response_sea_status = requests.get(url_sea_status)

# Continue if status is 200
if response_sea_status.status_code == 200:
    print("Sea status check passed.")
else:
    print(f"Failed to check sea status: {response_sea_status.status_code}")
    exit(1)

# Step 3: Check if fish list is empty
url_fish_list = f"http://localhost:8000/sea/{sea_id}/fish"
response_fish_list = requests.get(url_fish_list)

if response_fish_list.status_code == 200:
    fish_list = response_fish_list.json()
    if not fish_list:  # If fish list is empty
        print("Fish list is empty, proceeding.")
    else:
        print("Fish list is not empty, stopping.")
        exit(1)
else:
    print(f"Failed to retrieve fish list: {response_fish_list.status_code}")
    exit(1)

# Step 4: Add fish to the sea
url_add_fish = f"http://localhost:8000/sea/{sea_id}/fish"
data_add_fish = {
    "name": "Test fish1",
    "description": "Test fish1 description",
    "data": {"skibidi": "test"},
}

response_add_fish = requests.post(
    url_add_fish, headers=headers, data=json.dumps(data_add_fish)
)

if response_add_fish.status_code == 200:
    print("Fish added successfully.")
    exit(0)
else:
    print(f"Failed to add fish: {response_add_fish.status_code}")
    exit(1)
