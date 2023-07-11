# Installation
Before you getting to clone the directory you must be sure that Kafka and Spark have been installed in your machine.

Here is some useful links to install Kafka and Spark.

### Install Kafka
https://medium.com/@SaiParvathaneni/kafka-multi-node-cluster-simplified-6cea0ba5f1dd

https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04

You may face some problem that back to java home, so you should add java home to kafka.service file

### Install Spark

https://towardsdev.com/apache-spark-for-dummies-part-1-architecture-and-rdds-db2e36e3e312

# Application

1- Clone the **Application** 

```
git clone https://github.com/ghyathmoussa/log_monitoring.git
```

2- Go to directory

```
cd log_monitoring
```

3- Change the paths and IP addresses

4- Start the Producer

For **windows**

```
python kafka_producer.py
```

For **linux** and **macOS**

```
python3 kafka_producer.py
```

5- Start the Consumer

For **windows**

```
python spark_streamming.py
```

For **linux** and **macOS**

```
python3 spark_streamming.py
```