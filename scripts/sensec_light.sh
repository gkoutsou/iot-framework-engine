#!/bin/bash
dir=`dirname $0`
#Specify project home directory.
HOME_PATH=`cd  $dir;cd ..;pwd`
LOG_DIR=priv/logs
LOG_JS_DIR=priv/logs
ES_PORT=9200
MY_PATH=`pwd`

if [[ ("$1" = "start") || ("$1" = "test_setup") ]]; then
    cd $HOME_PATH
    echo "starting rabbit"
    make run_rabbit &
    echo $! >> $HOME_PATH/.temp.log
    echo "starting ES"
    make run_es &
    echo $! >> $HOME_PATH/.temp.log
    sleep 7
    echo "Starting IoT-Framework"
    export R_HOME="/usr/lib/R"
    sleep 3
    curl -XPUT localhost:$ES_PORT/sensorcloud
    if [ "$1" = "start" ]; then
	if [ -d "$LOG_DIR" ]; then
	    erl -noshell -pa $HOME_PATH/ebin/ $HOME_PATH/lib/*/ebin/ $HOME_PATH/lib/*/bin/ -boot start_sasl -s reloader -s engine -sname engine -config $HOME_PATH/config/engine.config > $LOG_DIR/sensor-cloud_log.log &
	else
	    erl -noshell -pa $HOME_PATH/ebin/ $HOME_PATH/lib/*/ebin/ $HOME_PATH/lib/*/bin/ -boot start_sasl -s reloader -s engine -sname engine -config $HOME_PATH/config/engine.config &
	fi
    fi
    echo $! >> $HOME_PATH/.temp.log
elif [ "$1" = "stop" ]; then
    echo "Closing nodejs and Sensor-Cloud"
    while read line
    do
	kill -- -$(ps opgid= $line | tr -d ' ')
    done < $HOME_PATH/.temp.log
    rm $HOME_PATH/.temp.log
fi

