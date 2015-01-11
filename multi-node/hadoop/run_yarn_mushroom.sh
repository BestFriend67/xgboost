#!/bin/bash
if [ "$#" -lt 3 ];
then
	echo "Usage: <nworkers> <nthreads> <path_in_HDFS>"
	exit -1
fi

# put the local training file to HDFS
hadoop fs -mkdir $3/data
hadoop fs -put ../../demo/data/agaricus.txt.train $3/data


python ../../rabit/tracker/rabit_yarn.py  -nw $1 -nt $2 -f ../../demo/data/agaricus.txt.test \
	-i $3/data/agaricus.txt.train -o $3/model  ../../xgboost mushroom.hadoop.conf  nthread=$2 dsplit=row



# get the final model file
hadoop fs -get $3/model/part-00000 ./final.model

# output prediction task=pred 
../../xgboost mushroom.hadoop.conf task=pred model_in=final.model \
    test:data=../../demo/data/agaricus.txt.test
# print the boosters of final.model in dump.raw.txt
../../xgboost mushroom.hadoop.conf task=dump model_in=final.model name_dump=dump.raw.txt
# use the feature map in printing for better visualization
../../xgboost mushroom.hadoop.conf task=dump model_in=final.model \
fmap=../../demo/data/featmap.txt name_dump=dump.nice.txt
cat dump.nice.txt
