#!/usr/bin/env python
import json
import redis
from kafka import KafkaProducer
from flask import Flask, request, jsonify


app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')
r = redis.Redis(host="redis",port="6379", db=0)

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/", methods=["GET"])
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

##########################################
## endpoints related to sword purchases ##
##########################################
#purchase a sword
@app.route("/sword", methods=["POST"])
def purchase_a_sword():
    #parse out data from payload
    request_data = request.get_json()
    user_name = request_data["user_name"]
    sword_name = request_data["sword_name"]

    #create an event
    purchase_item_event = {'event_type': 'purchase_sword',
                         'sword_name': sword_name,
                         'user_name': user_name,
                           }
    #log to kafka
    log_to_kafka('events', purchase_item_event)

    #update redis
    r.lpush("inventory:{}".format(user_name), sword_name)

    #return message to user
    message = jsonify({"message": "Successfully purchased a sword({}) for user({})".format(sword_name, user_name)})
    return message

##########################################
## endpoints related to money           ##
##########################################
#earn money
@app.route("/money", methods=["POST"])
def earn_money():
    #parse out data from payload
    request_data = request.get_json()
    user_name = request_data["user_name"]
    amount = int(request_data["amount"])
    
    #create an event
    earn_money_event = {'event_type': 'earn_money',
                        'user_name': user_name,
                        'amount': amount,
                        }
    #log to kafka
    log_to_kafka("events", earn_money_event)

    #update redis
    current_amount = r.get("user-money:{}".format(user_name))
    if current_amount is None:
        r.set("user-money:{}".format(user_name), amount)
    else:
        r.set("user-money:{}".format(user_name), amount+int(current_amount))

    #return message to user
    message = jsonify({"message": "User({}) earned ${}.)".format(user_name, amount)})
    return message

#spend money
@app.route("/money", methods=["DELETE"])
def spend_money():
    #parse out data from payload
    request_data = request.get_json()
    user_name = request_data["user_name"]
    amount = int(request_data["amount"])
    
    #create an event
    spend_money_event = {'event_type': 'spend_money',
                        'user_name': user_name,
                        'amount': amount,
                        }
    #log to kafka
    log_to_kafka("events", spend_money_event)

    #update redis
    current_amount = r.get("user-money:{}".format(user_name))
    if current_amount is None:
        r.set("user-money:{}".format(user_name), amount)
    else:
        current_amount = int(current_amount)
        if current_amount < amount:
            message = jsonify({"message": "does not have enough money -- current_money:({})".format(current_amount)})
            return message
        r.set("user-money:{}".format(user_name), amount-int(current_amount))

    #return message to user
    message = jsonify({"message": "User({}) spent ${}.)".format(user_name, amount)})
    return message


##########################################
## endpoints related to guilds          ##
##########################################

#join a guild
@app.route("/guild", methods=["PUT"])
def join_a_guild():
    #parse out data from payload
    request_data = request.get_json()
    user_name = request_data["user_name"]
    guild_name = request_data["guild_name"]

    #create an event
    join_guild_event = {'event_type': 'join_guild',
                         'guild_name': guild_name,
                         'user_name': user_name,
                       }
    #log to kafka
    log_to_kafka("events", join_guild_event)

    #update redis
    r.sadd("guild:{}".format(guild_name), user_name)
    r.set("user-guild:{}".format(user_name), guild_name)
    #return message to user
    message = jsonify({"message": "User({}) successfully joined a guild({})".format(user_name, guild_name)})
    return message

#leave a guild
@app.route("/guild", methods=["DELETE"])
def leave_a_guild():
    #parse out data from payload
    request_data = request.get_json()
    user_name = request_data["user_name"]
    guild_name = request_data["guild_name"]

    #create an event
    leave_guild_event = {'event_type': 'join_guild',
                         'guild_name': guild_name,
                         'user_name': user_name,
                       }
    
    #log to kafka
    log_to_kafka("events", leave_guild_event)

    #update redis
    r.srem("guild:{}".format(guild_name), user_name)
    r.set("user-guild:{}".format(user_name), "")

    #return message to user
    message = jsonify({"message": "User({}) successfully left a guild({})".format(user_name, guild_name)})
    return message

#view user status
@app.route("/user/<string:user_name>")
def view_status(user_name):
    
    #view status
    status = {}
    status["inventory"] = r.lrange("inventory:{}".format(user_name), 0, -1)
    status["guild"] =     r.get("user-guild:{}".format(user_name))
    status["money"] =     r.get("user-money:{}".format(user_name))
    
    #return message to user
    message = jsonify(status)
    return message
