# Files

| index | filename              | description                                                                                                                                      |
|-------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | docker-compose.yml    | docker compose file for starting up the data pipeline                                                                                            |
| 2     | Dockerfile            | docker file which installs redis python package into midsw205/base<br>:0.1.9                                                                     |
| 3     | game_api.py           | python file for starting Flask webserver                                                                                                         |
| 4     | tracking_events.py    | python file which defines custom schema for Spark streaming engine                                                                               |
| 5     | write_spark_stream.py | python file which starts up the Spark streaming engine                                                                                           |
| 6     | write_hive_table.py   | python file which writes the table meta-data to hive                                                                                             |
| 7     | drminix-history.txt   | history file which contains shell commands. Please see report.ipynb for annoated history                                                         |
| 8     | generate_events.sh    | bash shell script used to emulate random user behaviors                                                                                          |
| 9     | *.json                | json file used to send POST/DELETE request to Flask server. <br>For example) user1_sword1.json represents an activity in which user1 buys sword1 |
| 10    | report.ipynb          | REPORT                                                                                                                                           |
| 11    | img/ folder            | images used in the report file                                                                                                                   |