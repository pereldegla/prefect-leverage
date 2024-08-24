FROM python:3.11.4-slim-bullseye
USER root

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y openjdk-11-jre-headless curl

COPY requirements.txt /packages/requirements.txt

WORKDIR /packages
RUN pip install -r requirements.txt

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV PYTHONHASHSEED=1
ENV APACHE_SPARK_MAJOR_VERSION="3.5"
ENV APACHE_SPARK_VERSION="3.5.0"
ENV HADOOP_VERSION="3.3.4"
ENV ICEBERG_VERSION="1.4.3"
ENV SPARK_HOME="/usr/local/lib/python3.11/site-packages/pyspark/"

RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${APACHE_SPARK_MAJOR_VERSION}_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-${APACHE_SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar -Lo ${SPARK_HOME}/jars/iceberg-spark-runtime-${APACHE_SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar

# Download Java AWS SDK
ENV AWSJAVASDK_VERSION=1.12.262
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWSJAVASDK_VERSION}/aws-java-sdk-bundle-${AWSJAVASDK_VERSION}.jar -Lo ${SPARK_HOME}/jars/aws-java-sdk-bundle-${AWSJAVASDK_VERSION}.jar

# Download Hadoop-AWS for org.apache.hadoop.fs.s3a.S3AFileSystem
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -Lo ${SPARK_HOME}/jars/hadoop-aws-${HADOOP_VERSION}.jar

RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar -Lo ${SPARK_HOME}/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

