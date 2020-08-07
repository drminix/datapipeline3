#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from tracking_events import (
    sword_event_schema, guild_event_schema, money_event_schema,
    is_sword_event, is_guild_event, is_money_event)

def redis_sinker(df, epoch_id):
    print(epoch_id)
def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    # sword events
    sword_purchases = raw_events \
        .filter(is_sword_event(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                sword_event_schema()).alias('json')) \
        .select('json.*')
    
    sink1 = sword_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_sword_events") \
        .option("path", "/tmp/sword_events") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    # guild events
    guild_events = raw_events \
        .filter(is_guild_event(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                guild_event_schema()).alias('json')) \
        .select('json.*')

    sink2 = guild_events \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guild_events") \
        .option("path", "/tmp/guild_events") \
        .trigger(processingTime="10 seconds") \
        .start()

    #money events
    money_events = raw_events \
    .filter(is_money_event(raw_events.value.cast('string'))) \
    .select(from_json(raw_events.value.cast('string'),
            money_event_schema()).alias('json')) \
    .select('json.*')

    sink3 = money_events \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_money_events") \
        .option("path", "/tmp/money_events") \
        .trigger(processingTime="10 seconds") \
        .start()
     
    # block until any one of them terminates
    spark.streams.awaitAnyTermination() 

if __name__ == "__main__":
    main()
