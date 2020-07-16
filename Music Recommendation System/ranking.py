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

parser = argparse.ArgumentParser(description='Training Parser')
parser.add_argument('--skip_print', type=bool)
parser.add_argument('--model', type=str)
parser.add_argument('--type', choices=['val', 'test'])
parser.add_argument('--distinct', type=str)
parser.add_argument('--labels', type=str)
args = parser.parse_args()

# Only enter this block if we're in main
def main(spark, txt):
    model = ALSModel.load('hdfs:/user/jm7955/' + args.model)
    distinct_users = spark.read.parquet('hdfs:/user/jm7955/%s.parquet' % args.distinct)

    print("distinct_users")
    print('finished writing in %d seconds' % int(timer() - start))
    #distinct_users.show()
    labels = spark.read.parquet('hdfs:/user/jm7955/%s.parquet' % args.labels)
    print("labels")
    #labels.show()
    print('finished writing in %d seconds' % int(timer() - start))

    predictions = model.recommendForUserSubset(distinct_users, 500)\
        .select('user', F.col('recommendations.item').alias('item'))
    print("predictions")
    #predictions.show()
    print('finished writing in %d seconds' % int(timer() - start))
    predictionsAndLabels = predictions.join(labels, ["user"], "inner").rdd.map(
        lambda tup: (tup[1], tup[2]))
    print("predictionsAndLabels")
    print('finished writing in %d seconds' % int(timer() - start))
    
    metrics = RankingMetrics(predictionsAndLabels)
    print('finished writing in %d seconds' % int(timer() - start))
        
    file = open(txt, 'w') 
 
    file.write('metrics.meanAveragePrecision: %s\n' % metrics.meanAveragePrecision)
    file.write('metrics.precisionAt(500) %s\n' % metrics.precisionAt(500))
    file.write('metrics.ndcgAt(500) %s\n' % metrics.ndcgAt(500))
    file.close()
# Only enter this block if we're in main
if __name__ == "__main__":
    txt = '%s_%s.txt' % (args.model, args.type)
    if args.skip_print or not os.path.isfile(txt):
        start = timer()
        # Create the spark session object
        spark = SparkSession.builder.appName('ranking').getOrCreate()
        
        # Call our main routine
        main(spark, txt)
        end = timer()
        print(end - start)