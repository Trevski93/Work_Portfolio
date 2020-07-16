#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS,ALSModel
import pyspark.sql.functions as F 
from pyspark.mllib.evaluation import RankingMetrics
from timeit import default_timer as timer
import argparse 
import os.path  

parser = argparse.ArgumentParser(description='Baseline Parser')
parser.add_argument('--labels', type=str)
args = parser.parse_args()

# Only enter this block if we're in main
def main(spark):
    val_df = spark.read.parquet('hdfs:/user/jm7955/test_full_indexed.parquet').drop('count')
    labels = spark.read.parquet('hdfs:/user/jm7955/%s.parquet' % args.labels)
    
    predictions = val_df.groupBy("item").count().orderBy("count", ascending=False).limit(500).collect()
    predictions = [row.item for row in predictions]
    print("predictions")
    #predictions.show()
    print('finished writing in %d seconds' % int(timer() - start))
    predictionsAndLabels = labels.rdd.map(lambda tup: (predictions, tup[1]))
    print("predictionsAndLabels")
    print('finished writing in %d seconds' % int(timer() - start))
    
    metrics = RankingMetrics(predictionsAndLabels)
    print('finished writing in %d seconds' % int(timer() - start))
     
    print('metrics.meanAveragePrecision: %s\n' % metrics.meanAveragePrecision)
    print('metrics.precisionAt(500) %s\n' % metrics.precisionAt(500))
    print('metrics.ndcgAt(500) %s\n' % metrics.ndcgAt(500))
# Only enter this block if we're in main
if __name__ == "__main__":
    start = timer()
    # Create the spark session object
    spark = SparkSession.builder.appName('ranking').getOrCreate()
    
    # Call our main routine
    main(spark)
    end = timer()
    print(end - start)