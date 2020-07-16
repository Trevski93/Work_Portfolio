#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer

# Only enter this block if we're in main
def read(dataset):
    fname = 'hdfs:/user/bm106/pub/project/cf_%s.parquet' % dataset
    return spark.read.parquet(fname).drop('__index_level_0__')

def transform_and_save(df, name, user_indexer_model, track_indexer_model):
    df = user_indexer_model.transform(df).drop("user_id")
    df = track_indexer_model.transform(df).drop("track_id")
    df.write.parquet("hdfs:/user/jm7955/%s.parquet" % name, mode='overwrite')
    
def main(spark):
    train_df = read('train')
    user_indexer = StringIndexer(inputCol="user_id", outputCol="user")
    user_indexer_model = user_indexer.fit(train_df)
    track_indexer = StringIndexer(inputCol="track_id", outputCol="item", handleInvalid="skip")
    track_indexer_model = track_indexer.fit(train_df)

    transform_and_save(train_df, 'train_full_indexed', user_indexer_model, track_indexer_model)
    transform_and_save(read('validation'), 'val_full_indexed', user_indexer_model, track_indexer_model)
    transform_and_save(read('test'), 'test_full_indexed', user_indexer_model, track_indexer_model)
        
        
# Only enter this block if we're in main
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('save_indexer').getOrCreate()

    # Call our main routine
    main(spark)