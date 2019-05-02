#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Part 1: supervised model testing

Usage:

    $ spark-submit supervised_test.py hdfs:/path/to/load/model.parquet hdfs:/path/to/file

'''


# We need sys to get the command line arguments
import sys

# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession

# TODO: you may need to add imports here
from pyspark.ml import PipelineModel
from pyspark.mllib.evaluation import MulticlassMetrics


def main(spark, model_file, data_file):
    '''Main routine for supervised evaluation

    Parameters
    ----------
    spark : SparkSession object

    model_file : string, path to store the serialized model file

    data_file : string, path to the parquet file to load
    '''

    ###
    # TODO: YOUR CODE GOES HERE
    # Instantiate metrics object
    model = PipelineModel.load(model_file)
    
    df = spark.read.parquet(data_file)
    df_mfcc = df.select("mfcc_00", "mfcc_01", "mfcc_02", "mfcc_03", "mfcc_04", "mfcc_05", "mfcc_06", "mfcc_07", "mfcc_08", "mfcc_09", "mfcc_10", "mfcc_11", "mfcc_12", "mfcc_13", "mfcc_14", "mfcc_15", "mfcc_16", "mfcc_17", "mfcc_18", "mfcc_19","genre")
    
    
    predictions = model.transform(df_mfcc)
    
    print("Final prediction columns should be here: ",predictions.columns)
    predictionAndLabels = predictions.select("prediction","label")
    
    unique_classes = [i.label for i in predictionAndLabels.select('label').distinct().collect()]
    
    for label in unique_classes: 
        metrics_df = predictionAndLabels[predictionAndLabels['Label'] == label].rdd
        metrics = MulticlassMetrics(metrics_df)
        precision = metrics.precision()
        recall = metrics.recall()
        f1Score = metrics.fMeasure()
        print("Statistics For Class",label,":")
        print("precicison = ", precision)
        print("recall = ", recall)
        print("f1Score = ", f1Score)
 
    # Instantiate metrics object
    predsAndLabels_rdd = predictionAndLabels.rdd
    metrics = MulticlassMetrics(predsAndLabels_rdd)   
    
    # Overall statistics
    precision = metrics.precision()
    recall = metrics.recall()
    f1Score = metrics.fMeasure()
    
    print("Overall Summary Stats")
    print("precision = ",precision)
    print("recall = ", recall)
    print("f1Score = ", f1Score)
    
    print("Weighted Summary Stats")
    print("Weighted recall = %s" % metrics.weightedRecall)
    print("Weighted precision = %s" % metrics.weightedPrecision)
    print("Weighted F(1) Score = %s" % metrics.weightedFMeasure())
    
    ###

    pass




# Only enter this block if we're in main
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('supervised_test').getOrCreate()

    # And the location to store the trained model
    model_file = sys.argv[1]

    # Get the filename from the command line
    data_file = sys.argv[2]

    # Call our main routine
    main(spark, model_file, data_file)
