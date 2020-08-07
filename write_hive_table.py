#!/usr/bin/env python
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from tracking_events import (
    sword_event_schema, guild_event_schema, money_event_schema,
    is_sword_event, is_guild_event, is_money_event)

def main():
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .enableHiveSupport() \
        .getOrCreate()

    raw_events = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()

    #(1) sword_events
    sword_purchases = raw_events \
        .filter(is_sword_event(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                sword_event_schema()).alias('json')) \
        .select('json.*')

    sword_purchases.printSchema()
    sword_purchases.show()

    sword_purchases.registerTempTable("extracted_swords_events")

    spark.sql("""
        create external table sword_events
        stored as parquet
        location '/tmp/sword_events'
        as
        select * from extracted_swords_events
    """)

    #(2) guild_events
    guild_events = raw_events \
        .filter(is_guild_event(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                guild_event_schema()).alias('json')) \
        .select('json.*')

    guild_events.printSchema()
    guild_events.show()

    guild_events.registerTempTable("extracted_guild_events")

    spark.sql("""
        create external table guild_events
        stored as parquet
        location '/tmp/guild_events'
        as
        select * from extracted_guild_events
    """)

    #(3) health_events
    health_events = raw_events \
    .filter(is_money_event(raw_events.value.cast('string'))) \
    .select(from_json(raw_events.value.cast('string'),
            money_event_schema()).alias('json')) \
    .select('json.*')

    health_events.printSchema()
    health_events.show()

    health_events.registerTempTable("extracted_money_events")

    spark.sql("""
        create external table money_events
        stored as parquet
        location '/tmp/money_events'
        as
        select * from extracted_money_events
    """)   

if __name__ == "__main__":
    main()
