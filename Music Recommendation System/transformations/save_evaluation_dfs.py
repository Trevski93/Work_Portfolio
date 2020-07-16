#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
from pyspark.sql import SparkSession
import pyspark.sql.functions as F 
import argparse     
from timeit import default_timer as timer
import operator
from pyspark.sql import Window

parser = argparse.ArgumentParser(description='Save Eval DFs Parser')
parser.add_argument('--type', choices=['test', 'val'])
parser.add_argument('--user', type=str)
parser.add_argument('--index_file', type=str)
args = parser.parse_args()

# Only enter this block if we're in main
def main(spark):
    start = timer()
    df = spark.read.parquet('hdfs:/user/%s/%s_%s.parquet' % (args.user, args.type, args.index_file))
    print('finished reading in %d seconds' % int(timer() - start))
    distinct_users = df.select('user').distinct()
    print('finished distincting in %d seconds' % int(timer() - start))
    suffix = 'distinct_%s_users_%s.parquet' % (args.type, args.index_file)
    print(suffix)
    distinct_users.write.parquet(suffix, mode='overwrite')
    print('finished writing in %d seconds' % int(timer() - start))

    w = Window.partitionBy('user').orderBy(df['count'].desc())

    labels = df.withColumn(
            'sorted_list', F.collect_list('item').over(w)
        )\
        .groupBy('user')\
        .agg(F.max('sorted_list').alias('item'))
    
    suffix = '%s_labels_%s.parquet' % (args.type, args.index_file)
    print(suffix)
    labels.write.parquet(suffix, mode='overwrite')
    print('finished writing in %d seconds' % int(timer() - start))

    labels.show()
        
# Only enter this block if we're in main
if __name__ == "__main__":
    # Create the spark session object
    spark = SparkSession.builder.appName('save evaluation dfs').getOrCreate()
    
    # Call our main routine
    main(spark)