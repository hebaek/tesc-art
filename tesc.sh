#!/bin/bash

case $1 in
    start)  /usr/local/src/tesc-art.py > /home/pi/data/tesc-art.log &
            ;;

    stop)   sudo kill -15 $(ps aux|grep tesc-art.py|awk '{print $2}')
            ;;

    reload) sudo kill -s HUP $(ps aux|grep tesc-art.py|awk '{print $2}')
            ;;

    kill)   sudo kill -9 $(ps aux|grep tesc-art.py|awk '{print $2}')
            ;;
esac
