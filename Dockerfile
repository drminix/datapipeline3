#Using midsw205/base:0.1.9 as a base image
FROM midsw205/base:0.1.9

#install redis python package to connect redis in memory db
RUN pip install redis
