# Final AiCore Project - Kafka and AWS Integration

## Table of Contents
- [Project Description](#project-description)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [File Structure](#file-structure)
- [License](#license)

## Project Description
This project focuses on integrating Kafka with AWS to manage data streaming and processing. Key components include connecting to an EC2 instance, setting up Kafka, integrating with AWS IAM, and creating Kafka topics. The aim is to demonstrate the ability to handle real-time data streams effectively using Kafka in conjunction with AWS services. Through this project, I've deepened my understanding of cloud-based data handling and streaming technologies.

## Installation Instructions
**Prerequisites:**
- AWS account
- EC2 instance set up
- Kafka installed on your system

**Steps:**
1. **Set up Key Pair for EC2:**
   Ensure the key pair (e.g., "keypair.pem") is not publicly viewable:
    ```bash
    chmod 400 "keypair.pem"
    ```
2. **Access the EC2 Instance:**
   ```bash
   ssh -i "key pair.pem" ec2-user@<EC2-instance-IP>
    ```
3. **Install Java and Kafka on EC2:**
    ```
    sudo yum install java-1.8.0
    wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
    ```
## Usage Instructions

1. **Connect to EC2 and Navigate to Kafka Folder:**
   Follow the installation steps to connect to your EC2 instance and navigate to the Kafka folder.

2. **Integrate IAM User and Set Environment Variable:**
    Download the IAM auth JAR and add it to your CLASSPATH.

3. **Configure Kafka and AWS MSK:**
   Edit `client.properties` as shown in the instructions for proper configuration.

4. **Create Kafka Topics:**
   Use the provided commands to create topics such as `0e2bc66a6297.pin`.

5. **Run the Python Script:**
   Execute the Python script to start data processing.

## S3 Bucket and MSK Connect Integration

**Note:** You do not need to create an S3 bucket, IAM role, or VPC Endpoint to S3 as they are pre-configured.

1. **Locate S3 Bucket:**
   Go to the S3 console and find the bucket with your UserId. The format should be `user-<your_UserId>-bucket`.

2. **Download and Copy Confluent.io S3 Connector:**
   On your EC2 client, perform the following steps to download the Confluent.io Amazon S3 Connector and copy it to your identified S3 bucket:

   ```bash
   # Assume admin user privileges
   sudo -u ec2-user -i
   
   # Create directory for the connector
   mkdir kafka-connect-s3 && cd kafka-connect-s3
   
   # Download connector from Confluent
   wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-s3/versions/10.0.3/confluentinc-kafka-connect-s3-10.0.3.zip
   
   # Copy connector to your S3 bucket
   aws s3 cp ./confluentinc-kafka-connect-s3-10.0.3.zip s3://user-<your_UserId>-bucket/kafka-connect-s3/

## Create Custom Plugin in MSK Connect

1. **Create Custom Plugin:**
   - Navigate to the MSK Connect console in your AWS account.
   - Create a custom plugin with the name: `<your_UserId>-plugin`.
   -use the .zip uploaded to s3 earlier

2. **Configure Bucket Name:**
   - Ensure the bucket name is correctly set to `user-<your_UserId>-bucket`.

3. **Set Topics Regex:**
   - In the connector configuration, set `topics.regex` to `<your_UserId>.*`.
   - This configuration ensures that data from Kafka topics is correctly routed to your S3 bucket.

4. **Select IAM Role for Permissions:**
   - When building the connector, choose the IAM role with the name `<your_UserId>-ec2-access-role`.
   - This role should have the necessary permissions for the connector to interact with both MSK and your S3 bucket.

```
connector.class=io.confluent.connect.s3.S3SinkConnector
# same region as our bucket and cluster
s3.region=us-east-1
flush.size=1
schema.compatibility=NONE
tasks.max=3
# include nomeclature of topic name, given here as an example will read all data from topic names starting with msk.topic....
topics.regex=<YOUR_UUID>.*
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
value.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
storage.class=io.confluent.connect.s3.storage.S3Storage
key.converter=org.apache.kafka.connect.storage.StringConverter
s3.bucket.name=<BUCKET_NAME>
```

## Steps and Commands for Setting Up Kafka REST Proxy Integration
Here are the commands and configuration details:

#### Create Method on AWS API
1. Add resource called `{proxy+}`
2. Add method to this HTTP, ANY, and public ipv4 of ec2 instance
3. Deploy
4. Invoke URL = ` http://ec2-54-145-77-91.compute-1.amazonaws.com:8082/{proxy}`

### Installing Confluent Package for REST Proxy on EC2 Client
```bash
ssh -i "KeyPair.pem" ec2-user@ec2-54-145-77-91.compute-1.amazonaws.com
```
```
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
tar -xvzf confluent-7.2.0.tar.gz
```
```
cd confluent-7.2.0/etc/kafka-rest
```
```
nano kafka-rest.properties
```
```
#id=kafka-rest-test-server
#schema.registry.url=http://localhost:8081
#zookeeper.connect=localhost:2181
bootsrap.servers=b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaw$
zookeeper.connect=z-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazona$
#bootstrap.servers=PLAINTEXT://localhost:9092
#
# Configure interceptor classes for sending consumer and producer metrics to Confluent Control Center
# Make sure that monitoring-interceptors-<version>.jar is on the Java class path
#consumer.interceptor.classes=io.confluent.monitoring.clients.interceptor.MonitoringConsumerInterceptor
#producer.interceptor.classes=io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor
# Sets up TLS for encryption and SASL for authN.
client.security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
client.sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="arn:aws:iam::584739742957:role/0e2bc66a6297-ec2-access-role";

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this clas
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
Add this to path
```
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```
Add this to .bashrc so it runs every time the instance starts
```
 nano ~/.bashrc

 #Add line
 export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```

## Start the server and use user_posting_emulation_API.py to test it 
### On the Ec2 Instance start the server
```
confluent-7.2.0/bin
```
```
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```
### On your local machine run the following python code to send data to the API
```
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
    

```

# Mounting to s3 with Databricks
1. create a new notebook in your databricks workspace
1. ```
   # pyspark functions
   from pyspark.sql.functions import *
   # URL processing
   import urllib
   ```
1. ```
   # Define the path to the Delta table
   delta_table_path = "dbfs:/user/hive/warehouse/authentication_credentials"

   # Read the Delta table to a Spark DataFrame
   aws_keys_df = spark.read.format("delta").load(delta_table_path)
      ```
1. ```
   # Get the AWS access key and secret key from the spark dataframe
   ACCESS_KEY = aws_keys_df.select('Access key ID').collect()[0]['Access key ID']
   SECRET_KEY = aws_keys_df.select('Secret access key').collect()[0]['Secret access key']
   # Encode the secrete key
   ENCODED_SECRET_KEY = urllib.parse.quote(string=SECRET_KEY, safe="")
   ```
1. ```
   # AWS S3 bucket name
   AWS_S3_BUCKET = "user-0e2bc66a6297-bucket"
   # Mount name for the bucket
   MOUNT_NAME = "/mnt/s3_bucket"
   # Source url
   SOURCE_URL = "s3n://{0}:{1}@{2}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_S3_BUCKET)
   # Mount the drive
   dbutils.fs.mount(SOURCE_URL, MOUNT_NAME)
   ```
1. ```
   display(dbutils.fs.ls("/mnt/s3_bucket/topics/0e2bc66a6297.pin/partition=0/"))
   ```
1. ```
   %sql
   SET spark.databricks.delta.formatCheck.enabled=false
   ```
1. ```
   # File location and type
   # Asterisk(*) indicates reading all the content of the specified file that have .json extension
   file_location = "/mnt/s3_bucket/topics/0e2bc66a6297.pin/partition=0/*.json" 
   file_type = "json"
   # Ask Spark to infer the schema
   infer_schema = "true"
   # Read in JSONs from mounted S3 bucket
   df = spark.read.format(file_type) \
   .option("inferSchema", infer_schema) \
   .load(file_location)
   # Display Spark dataframe to check its content
   display(df)
   ```

### all databricks notebooks can be found in  `./databricks-notebooks`

## Reading from S3 with Databricks

This section explains how to read data from an S3 bucket using Databricks.

1. **Listing Files in S3 Bucket**: 
   ```python
   display(dbutils.fs.ls("/mnt/s3_bucket/topics/0e2bc66a6297.pin/partition=0/"))
   ```
   This command lists all the files in the specified directory of the S3 bucket. It's useful for verifying the files you want to process are present.

2. **Setting Spark Configuration**:
   ```
   %sql
   SET spark.databricks.delta.formatCheck.enabled=false
   ```
   This SQL command disables the Delta format check in Spark. It's useful when dealing with non-Delta format files.

3. **eading JSON Files from S3 Bucket:**:
   ```
   # File location and type
   # Asterisk(*) indicates reading all the content of the specified file that have .json extension
   file_location = "/mnt/s3_bucket/topics/0e2bc66a6297.pin/partition=0/*.json" 
   file_type = "json"
   # Ask Spark to infer the schema
   infer_schema = "true"
   # Read in JSONs from mounted S3 bucket
   posts_df = spark.read.format(file_type) \
   .option("inferSchema", infer_schema) \
   .load(file_location)
   # Display Spark dataframe to check its content
   display(posts_df)
   ```

   This Python snippet reads all JSON files from the specified location in the mounted S3 bucket. It infers the schema of the JSON files automatically and loads them into a Spark DataFrame, which is then displayed.

## Cleaning Data

#### Pinterest Geolocation Data Cleaning
- **File**: `pinterest-geolocation-data-cleaning.ipynb`
- **Key Steps**:
  1. Create a new column `coordinates` based on `latitude` and `longitude` columns.
  2. Drop the `latitude` and `longitude` columns.
  3. Convert `timestamp` from string to timestamp data type.
  4. Reorder DataFrame columns to `ind`, `country`, `coordinates`, `timestamp`.
  5. Replace irrelevant data in each column with `None`.

#### Pinterest Posts Data Cleaning
- **File**: `pinterest-posts-data-cleaning.ipynb`
- **Key Steps**:
  1. Replace empty or irrelevant entries in each column with `None`.
  2. Transform `follower_count` to ensure numeric entries and convert to `int`.
  3. Ensure numeric columns have numeric data types.
  4. Clean `save_location` to include only the path.
  5. Rename `index` column to `ind`.
  6. Reorder DataFrame columns to include `ind`, `unique_id`, `title`, `description`, `follower_count`, `poster_name`, `tag_list`, `is_image_or_video`, `image_src`, `save_location`, `category`.

#### Pinterest User Data Cleaning
- **File**: `pinterest-user-data-cleaning.ipynb`
- **Key Steps**:
  1. Create a new column `user_name` by concatenating `first_name` and `last_name`.
  2. Drop `first_name` and `last_name` columns.
  3. Convert `date_joined` from string to timestamp data type.
  4. Reorder DataFrame columns to `ind`, `user_name`, `age`, `date_joined`.
  5. Replace irrelevant data in each column with `None`.

## Querying Cleaned Data
- **File**: `querying-cleaned-data.ipynb`
- **Key Steps**:
  1. Query to find the most popular Pinterest category based on country, returning columns for country, category, and category count.
  2. Drop duplicate rows and group by country and category to count the number of posts.
  3. Filter category counts greater than 1 and order the table in descending order.
  4. Use window specification to assign ranks within each country partition and keep only the top category for each country.
  5. Query to determine the number of posts each category had between 2018 and 2022, with columns for post year, category, and category count.
  6. Extract the year from timestamp, group by year and category, and sum posts for each category per year.
  7. Join geo and user tables, followed by a join with post tables. Select appropriate columns and apply window specification for ranking.
  8. Create age groups and group data by age group and category to find trends.
  9. Use window specification for ranking within country partitions.
  10. Calculate mean follower count grouped by age group.
  11. Extract year from timestamp for posts within a specified range of years.

## Batch Processing with AWS MWAA
### The following steps outline how to created a dag for apache airflow to run Databricks notebooks

Get cluster id from databricks notebook 

```
spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
```

Get path from databricks notebook 

```
dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
```
### create dag.py
```
../databricks-airflow/0e2bc66a6297_dag
```
### Upload dag to correct bucket in s3
To test the DAG Access the Managed Apache Airflow GUI in AWS to enable and run the DAG manually. 

# Stream Processing: AWS Kinesis
This section provides a concise overview of the configuration and use of AWS Kinesis for streaming data related to Pinterest tables in real time.

### Steps
1. **Creating Data Streams**
   - Three Kinesis data streams are created in the AWS GUI for different types of Pinterest data:
     - `streaming-<your_UserId>-pin` for Pinterest pin data.
     - `streaming-<your_UserId>-geo` for geographical information.
     - `streaming-<your_UserId>-user` for user data.
   - More detailed instructions can be found [Here](https://colab.research.google.com/github/AI-Core/Content-Public/blob/main/Content/units/Cloud-and-DevOps/3.%20Essential%20Cloud%20Technology/12.%20AWS%20Kinesis/Notebook.ipynb)

2. **Configuring REST API for Kinesis Actions**
   - A REST API is configured to allow interaction with Kinesis, supporting operations such as stream listing, creation, description, deletion, and record addition.
   - Permissions for these actions are facilitated through the IAM role named `<your_UserId-kinesis-access-role>`. This role's ARN is used in setting up the execution role for the API's integration points.
   - More detailed instructions can be found [Here](
   https://colab.research.google.com/github/AI-Core/Content-Public/blob/main/Content/units/Cloud-and-DevOps/4.%20AWS%20Serverless%20API%20Stack/3.%20Integrating%20API%20Gateway%20with%20Kinesis/Notebook.ipynb)

3. **Script for Data Streaming**
   - The `user_posting_emulation_streaming.py` script is introduced to send data to the configured Kinesis streams. It ensures the data from each Pinterest table is appropriately streamed to its designated Kinesis stream. 
   - The follwoing outlines the method added to the 'user_posting_emulation.py' to emulate streaming.
   ```
   def stream_to_API(stream_name, partition_key, result):
    invoke_url = f"https://iijg6a7epl.execute-api.us-east-1.amazonaws.com/Development/streams/{stream_name}/record"
    #To send JSON messages you need to follow this structure
    payload = json.dumps({
    "StreamName": stream_name,
    "Data":  result,
            "PartitionKey": partition_key
            })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("PUT", invoke_url, headers=headers, data=payload)
    print(response)
    return response
    ```
    ```
    stream_to_API("streaming-0e2bc66a6297-pin", "partition-1", pin_result)
    ```

4. **Read data from from kinesis streams to Databricks**:
   This section outlines the process of reading AWS credentials from a Delta table and setting up Spark streaming reads from Kinesis streams using PySpark. The code for the follwoing steps can be found at ./databricks-notebooks/read-from-kinesis.ipynb

   ### Reading AWS Credentials

   **Imports**: The script begins by importing necessary PySpark SQL types and functions, along with the `urllib` library for URL encoding.

   **Delta Table Path**: It defines the path to a Delta table storing AWS credentials (`dbfs:/user/hive/warehouse/authentication_credentials`).

   **Read Delta Table**: AWS credentials are read into a Spark DataFrame (`aws_keys_df`) using the Delta format.

   **Extract Credentials**: The script extracts `Access key ID` and `Secret access key` from the DataFrame, indicating the table contains these specific columns.

   **Encode Secret Key**: The `Secret access key` is URL-encoded using `urllib.parse.quote` for safe inclusion in URLs/API requests.

   ### Setting Up Spark Streaming

   1. **Disable Delta Format Check**: A SQL command is used to disable format checks for Delta tables, which may be necessary for compatibility or performance reasons.

   2. **Kinesis Stream Reads**: The script configures Spark to read from Kinesis streams (`geo_stream`, `pin_stream`, `user_stream`) using the extracted and encoded AWS credentials. Each stream read is configured with:
      - The stream name (e.g., `streaming-0e2bc66a6297-geo`).
      - The initial position set to `earliest` for reading from the start of the stream.
      - The AWS region (e.g., `us-east-1`).
      - AWS access and secret keys for authentication.

   3. **Data Processing**: For each stream, data is cast to a string format for further processing or analysis.

5. **Transform Kinesis streams in databricks**
One the spark streams have been created we are able to transform the data in the same manner outlined in the 'cleaning data section' passing the streams to their respecive cleaning methods in the dollowing Databricks notebooks.
   ```
   pinterest-user-data-cleaning.ipynb
   ```
   ```
   pinterest-pin-data-cleaning.ipynb
   ```
   ```
   pinterest-geo-data-cleaning.ipynb
   ```

6. **Write streaming data to delta tables**:
Once the data has been transfomed it can be written to a Delta table in Databricks using the method below:
   ```
   def write_to_delta(table, table_name):
   table.writeStream \
      .format("delta") \
      .outputMode("append") \
      .option("checkpointLocation", "/tmp/kinesis/_checkpoints/") \
      .table(table_name)
   ```

## File Structure
```
project-root/
│
├── databricks-notebooks/
│ ├── AirFlow/
│ │ └── DailyDag.ipynb
│ │
│ ├── Kinesis/
│ │ ├── clean-streaming-data-geo.ipynb
│ │ ├── clean-streaming-data-pin.ipynb
│ │ ├── clean-streaming-data-user.ipynb
│ │ ├── main.ipynb
│ │ ├── read-from-kinesis.ipynb
│ │ └── write-to-delta-table.ipynb
│ │
│ └── s3/
│ ├── mounting-to-s3.ipynb
│ └── reading-from-s3.ipynb
│
├── spark/
│ ├── pinterest-geolocation-data-cleaning.ipynb
│ ├── pinterest-posts-data-cleaning.ipynb
│ ├── pinterest-user-data-cleaning.ipynb
│ └── querying-cleaned-data.ipynb
│
├── Python/
│ └── api_response.py
| ├── KeyPair.pem
| ├── keyPairName.pem
| ├── rdsCreds.py
| ├── s3Creds.py
| ├── user_posting_emulation_initial.py
| ├── user_posting_emulation_streaming_initial.py
| ├── user_posting_emulation_streaming.py
| ├── user_posting_emulation.py
├── .gitignore
├── follow_along.md
└── readme.md

```

## License
```
License details go here
```