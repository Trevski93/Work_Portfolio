#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import random 
import itertools
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from timeit import default_timer as timer
import argparse     

parser = argparse.ArgumentParser(description='Training Parser')
parser.add_argument('--user', type=str)
parser.add_argument('--train_file', type=str)
parser.add_argument('--alpha', type=float)
parser.add_argument('--rank', type=int)
parser.add_argument('--reg', type=float)
parser.add_argument('--all_or_one', choices=['all', 'one'])
parser.add_argument('--start', type=int)
parser.add_argument('--end', type=int)
args = parser.parse_args()

def getwritefile(write_prefix, rank, reg, alpha):
    suffix = 'implicit_rank_%d_reg_%s_alpha_%s' % (rank, reg, alpha)
    writefile = write_prefix + suffix
    print('training for %s' % writefile)
    return writefile, suffix

def already_trained(spark, path):
    try:
        rdd = spark.sparkContext.textFile(path)
        rdd.take(1)
        print('already trained')
        return True
    except Py4JJavaError as e:
        return False

def get_train_df():
    return spark.read.parquet('hdfs:/user/jm7955/%s.parquet' % args.train_file)

def train(df, writefile, rank, reg, alpha):
    start = timer()
    als = ALS(regParam=reg, rank=rank, alpha=alpha, ratingCol="count", implicitPrefs=True)
    model = als.fit(df)
    print('finished training in %d seconds' % int(timer() - start))
    model.save(writefile)
    print('finished training and writing in %d seconds' % int(timer() - start))

def train_one(write_prefix, args):
    writefile, suffix = getwritefile(write_prefix, args.rank, args.reg, args.alpha)
    # if already_trained(spark, suffix):
    #     print(5)
    #     return
    print(6)    

    train(get_train_df(), writefile, args.rank, args.reg, args.alpha)

def train_all(write_prefix):
    train_df = get_train_df()
    ranks = (10, 30, 50)
    regs = (.01, .1, 1.0)
    alphas = (0.5, 1.0, 5.0)
    params_list = list(itertools.product(ranks, regs, alphas))

    count = 0
    for params in params_list:
        writefile, suffix = getwritefile(write_prefix, *params)
        if args.start <= count <= args.end:
            train(train_df, writefile, *params)
        count += 1
# Only enter this block if we're in main
def main(spark):
    write_prefix = 'hdfs:/user/%s/als_implicit_%s_' % (args.user, args.train_file)

    if args.all_or_one == 'one':
        print(3)
        train_one(write_prefix, args)
    else:
        print(4)
        train_all(write_prefix)

# Only enter this block if we're in main
if __name__ == "__main__":
    print(1)
    # Create the spark session object
    spark = SparkSession.builder.appName('train').getOrCreate()
    print(2)
    # Call our main routine
    main(spark)