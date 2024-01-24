import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from rdsCreds import RDS_HOST, RDS_PASSWORD, RDS_USER
random.seed(100)

class AWSDBConnector:

    def __init__(self):

        self.HOST = RDS_HOST
        self.USER = RDS_USER
        self.PASSWORD = RDS_PASSWORD
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine

new_connector = AWSDBConnector()

def post_to_API(topic_name, result):
    proxy="{proxy+}"
    invoke_url = f"https://iijg6a7epl.execute-api.us-east-1.amazonaws.com/Development/topics/{topic_name}"
    payload = json.dumps({
    "records": [
        {
        #Data should be send as pairs of column_name:value, with different columns separated by commas       
        "value": result
        }
    ]
    })
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    response = requests.request("POST", invoke_url, headers=headers, data=payload)
    print(response)
    return response

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            print(pin_result)
            post_to_API("0e2bc66a6297.pin", pin_result)
            # {'index': 8304, 'unique_id': '5b6d0913-25e4-43ab-839d-85d5516f78a4', 'title': 'The #1 Reason You’re Not His Priority Anymore - Matthew Coast', 'description': '#lovequotes #matchmaker #matchmadeinheaven #loveyourself #respectyourself', 'poster_name': 'Commitment Connection', 'follower_count': '51k', 'tag_list': 'Wise Quotes,Quotable Quotes,Words Quotes,Wise Words,Quotes To Live By,Great Quotes,Motivational Quotes,Inspirational Quotes,Funny Quotes', 'is_image_or_video': 'image', 'image_src': 'https://i.pinimg.com/originals/c6/64/ee/c664ee71524fb5a6e7b7b49233f93b43.png', 'downloaded': 1, 'save_location': 'Local save in /data/quotes', 'category': 'quotes'}
            print(geo_result)
            # post_to_API("0e2bc66a6297.geo", geo_result)
            # {'ind': 7528, 'timestamp': datetime.datetime(2020, 8, 28, 3, 52, 47), 'latitude': -89.9787, 'longitude': -173.293, 'country': 'Albania'}
            print(user_result)
            # post_to_API("0e2bc66a6297.user", user_result)
            # {'ind': 2863, 'first_name': 'Dylan', 'last_name': 'Holmes', 'age': 32, 'date_joined': datetime.datetime(2016, 10, 23, 14, 6, 51)}


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    

# #To send JSON messages you need to follow this structure
# payload = json.dumps({
#     "records": [
#         {
#         #Data should be send as pairs of column_name:value, with different columns separated by commas       
#         "value": {"index": example_df["index"], "name": example_df["name"], "age": example_df["age"], "role": example_df["role"]}
#         }
#     ]
# })

# headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
# response = requests.request("POST", invoke_url, headers=headers, data=payload)
