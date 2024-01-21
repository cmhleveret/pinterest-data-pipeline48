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

# License
```
License details go here
```