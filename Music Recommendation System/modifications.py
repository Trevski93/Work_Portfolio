#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession
from pyspark.sql.functions import log

# Only enter this block if we're in main
    
def log_calc(df):
    df = df.withColumn("count", log(df["count"] + 1))
    return df

def dropLowCount(df,k):
    df = df.filter(train_df['count'] > k)
    return df
    
def main(spark): 
    dataset = spark.read.parquet('hdfs:/user/jm7955/train_full_indexed.parquet')
    
    #take log of count values
    log_set = log_calc(dataset)
    log_set.write.parquet("hdfs:/user/tim225/train_log.parquet", mode='overwrite')
    
    #drop low count values
    high_count = dropLowCount(dataset,1)
    high_count.write.parquet("hdfs:/user/tim225/train_hc.parquet", mode='overwrite')
    
    #take of count values and drop low count values
    drop_low_set  = dropLowCount(dataset,1)
    drop_low_log = log_calc(drop_low_set)
    drop_low_log.write.parquet("hdfs:/user/tim225/train_log_hc.parquet", mode='overwrite')
    
    
     
        
# Only enter this block if we're in main
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('modifications').getOrCreate()

    # Call our main routine
    main(spark)