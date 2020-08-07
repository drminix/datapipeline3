#!/bin/bash

while true; do

    #generate a random transactions
    NUM=$((($RANDOM%10)+1)) 
    echo "Purchasing $NUM bigsword1 for user1"
    docker-compose exec mids ab -p "/w205/project-3-drminix/user1_sword1.json" -T application/json -n $NUM  http://localhost:5000/sword
    NUM=$((($RANDOM%10)+1)) 
    echo "Purchasing $NUM smallsword2 for user1"
    docker-compose exec mids ab -p "/w205/project-3-drminix/user1_sword2.json" -T application/json -n $NUM  http://localhost:5000/sword
    NUM=$((($RANDOM%10)+1)) 
    echo "Purchasing $NUM bigsword1 for user2"
    docker-compose exec mids ab -p "/w205/project-3-drminix/user2_sword1.json" -T application/json -n $NUM  http://localhost:5000/sword
    NUM=$((($RANDOM%10)+1)) 
    echo "Purchasing $NUM smallsword2 for user1"
    docker-compose exec mids ab -p "/w205/project-3-drminix/user2_sword2.json" -T application/json -n $NUM  http://localhost:5000/sword
    
    #randomly earn money
    NUM=$(($RANDOM%100))
    if [ $NUM -lt 10 ] #earn money
        then 
        echo "Earned 10 dollars for user1"
        docker-compose exec mids ab -p "/w205/project-3-drminix/user1_earn10.json" -T application/json -n $NUM  http://localhost:5000/money
    else
        echo "Not earned any money for user1"
    fi

    #randomly join a guild
    if [ $NUM -lt 5 ] # number 0 ~ 4
        then
            echo "User1 joins guild1"
            docker-compose exec mids ab -u "/w205/project-3-drminix/user1_guild1.json" -T application/json -n 1 http://localhost:5000/guild
    elif [ $NUM -lt 10 ] #number 5~ 9
        then
            echo "User1 joins guild2"
            docker-compose exec mids ab -u "/w205/project-3-drminix/user1_guild2.json" -T application/json -n 1  http://localhost:5000/guild
    else
        echo "Not joining any guild"
    fi
    
    sleep 5
done
