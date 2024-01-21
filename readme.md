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

# License
```
License details go here
```