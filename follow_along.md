# Final AiCore project



# Connect to EC2
Run this command, if necessary, to ensure your key is not publicly viewable.

```
chmod 400 "key pair.pem"
```

Acces the EC2 instance
```
ssh -i "key pair.pem" ec2-user@ec2-54-145-77-91.compute-1.amazonaws.com
```

Install Java
```
sudo yum install java-1.8.0
wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
```

Navigate to Kafka folder
```
cd kafka_2.12-2.8.1
cd libs
```

Integrate IAM user
```
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar
```
Add this to path
```
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```


# Cluster auth ARM: 

Copy ARN:
arn:aws:iam::584739742957:role/0e2bc66a6297-ec2-access-role

navigate to 
```
cd kafka_2.12-2.8.1/bin
```
```
nano client.properties
```
```
# Sets up TLS for encryption and SASL for authN.
security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="arn:aws:iam::584739742957:role/0e2bc66a6297-ec2-access-role";

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

# Create a topic on a client machine
```
cd kafka_2.12-2.8.1/bin
```

In the AWS GUI go to 

Clusters>pinterest-msk-cluster>View client information

Bootstrap servers string
```
b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098
```

Plaintext Apache Zookeeper connection string
```
z-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181
```

You will need to create the following three topics

```
./kafka-topics.sh --bootstrap-server b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 0e2bc66a6297.pin
```
```
./kafka-topics.sh --bootstrap-server b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 0e2bc66a6297.geo
```
```
./kafka-topics.sh --bootstrap-server b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 0e2bc66a6297.user
```