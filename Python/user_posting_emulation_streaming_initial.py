import requests
import json

example_df = {"index": 1, "name": "Maya", "age": 25, "role": "engineer"}

# invoke url for one record, if you want to put more records replace record with records
invoke_url = "https://iijg6a7epl.execute-api.us-east-1.amazonaws.com/Development/streams/{stream-name}/record"


#To send JSON messages you need to follow this structure
payload = json.dumps({
    "StreamName": "YourStreamName",
    "Data": {
            #Data should be send as pairs of column_name:value, with different columns separated by commas      
            "index": example_df["index"], "name": example_df["name"], "age": example_df["age"], "role": example_df["role"]
            },
            "PartitionKey": "desired-name"
            })

headers = {'Content-Type': 'application/json'}

response = requests.request("PUT", invoke_url, headers=headers, data=payload)
