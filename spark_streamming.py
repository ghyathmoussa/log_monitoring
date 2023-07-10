from pyspark.sql import SparkSession
# from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType, StringType
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
# to set the configuration of kafka with spark
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

spark = SparkSession.builder.appName('log monitoring streamer').master('local[*]').getOrCreate()

@udf(returnType=BooleanType())
def contains_error(line):
    line_json = json.loads(line)
    return 'ERROR' in line_json['log_line']

# Send email
@udf(returnType=StringType())
def send_email_alert(line):
    error_line = json.loads(line)['log_line']
    
    # Email content
    msg = MIMEMultipart()
    msg['From'] = 'ghyathmoussa11@gmail.com'
    msg['To'] = 'ghyathmoussa@hotmail.com'
    msg['Subject'] = 'Log Monitor Alert'
    message = f'ERROR found: {error_line}'
    msg.attach(MIMEText(message))

    # Send the email
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('your_mail@gmail.com', 'password')
    mailserver.sendmail('your_mail@gmail.com', 'received_mail@gmail.com', msg.as_string())
    mailserver.quit()

    return 'Email Alert sent.'

# sign to kafka topic

df = spark.readStream.format('kafka').option("kafka.bootstrap.servers", "kafka-ip-address:port").option("subscribe", "your-topic").load()

# Filter the lines that contain 'ERROR'
error_lines = df.filter(contains_error(col("value")))

# send msg
#alert = error_lines.withColumn("Alert", send_email_alert(col("value")))

alert = error_lines.withColumn("Alert", col("value"))

# Write the 'ERROR' lines and Alert to console
query = alert.writeStream.outputMode("append").format("console").start()

query.awaitTermination()

print(df.show())
