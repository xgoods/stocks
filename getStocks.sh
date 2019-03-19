#!/bin/bash

function getStocks() {
    date=`date +%Y-%m-%d`
    wget "http://online.wsj.com/mdc/public/page/2_3021-activcomp-actives.html" -O "${date}.html"
    python DomParse.py $date.html
}

x=0

while [[ $x -le 60 ]]
do
    getStocks
    sleep 60
    $x = `expr $x + 1`
done


