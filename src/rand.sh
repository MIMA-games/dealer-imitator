#!/bin/bash

b=0

while [ "$b" -lt "$3" ]; do
    my_array=()
    a=0
    while [ "$a" -lt "$1" ]; do
        result=$(od -An -N1 -tu1 < /dev/urandom)
        
        if [ "$result" -lt "$2" ]; then
            my_array+=("$result")
            a=$((a + 1))
        fi
    done
    b=$((b + 1))
    echo ${my_array[*]}
done
