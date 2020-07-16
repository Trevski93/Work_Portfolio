#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random 
import itertools

# And pyspark.sql to get the spark session
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
#from pyspark.ml import Pipeline

def read(dataset):
    fname = 'hdfs:/user/bm106/pub/project/cf_%s.parquet' % dataset
    return spark.read.parquet(fname).drop('__index_level_0__')

def transform_and_save(df, name, user_indexer_model, track_indexer_model):
    df = user_indexer_model.transform(df).drop("user_id")
    print('11')
    df = track_indexer_model.transform(df).drop("track_id")
    print('12')
    df.write.parquet("hdfs:/user/jm7955/%s.parquet" % name, mode='overwrite')
    print('13')

def main(spark):
    train_df = read('train')
    print('1')
    test_df = read('test')
    print('2')
    val_df = read('validation')
    print('3')
    val_test_df = val_df.union(test_df)
    
    user_indexer = StringIndexer(inputCol="user_id", outputCol="user", handleInvalid="skip")
    user_indexer_model = user_indexer.fit(val_test_df)
    in_val_test_df = user_indexer_model.transform(train_df).drop("user")
    print('4')
    
    user_indexer_model.setHandleInvalid("keep")
    train_df = user_indexer_model.transform(train_df)
    print('6')
    out_of_val_test_idx = train_df.agg({"user": "max"}).collect()[0][0]
    print('7')
    out_of_val_test_df = train_df.filter(train_df.user == out_of_val_test_idx).drop("user")
    print('8')

    out_of_val_test_df.createOrReplaceTempView('out_of_val_test')

    user_ids_str = 'SELECT DISTINCT user_id FROM out_of_val_test' 
    user_cnt = spark.sql(user_ids_str).count()
    down_sample_rate = 30
    sub_user_ids_str = 'SELECT * from (%s ORDER BY RAND() LIMIT %d)' % (user_ids_str, user_cnt/down_sample_rate)
    sub_sample_df = spark.sql('SELECT * FROM out_of_val_test where user_id IN (%s)' % sub_user_ids_str)
    print('9')

    sub_sample_df = sub_sample_df.union(in_val_test_df)
    print('10')

    user_indexer_model = user_indexer.fit(sub_sample_df)
    track_indexer = StringIndexer(inputCol="track_id", outputCol="item", handleInvalid="skip")
    track_indexer_model = track_indexer.fit(sub_sample_df)

    transform_and_save(sub_sample_df, 'sub_train_%d' % down_sample_rate, user_indexer_model, track_indexer_model)
    transform_and_save(val_df, 'val_sub_indexed_%d' % down_sample_rate, user_indexer_model, track_indexer_model)
    transform_and_save(test_df, 'test_sub_indexed_%d' % down_sample_rate, user_indexer_model, track_indexer_model)
    
# Only enter this block if we're in main
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('subsample').getOrCreate()

    # Call our main routine
    main(spark)