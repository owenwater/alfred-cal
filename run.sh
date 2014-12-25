#!/bin/bash

query="$1"

if [[ "$query" == *.json ]]
then
    open "$query"
else
    osascript open_cal.scpt "$query"
fi

